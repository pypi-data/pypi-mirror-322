from __future__ import annotations
from datetime import datetime
from enum import StrEnum
import hashlib
from pickle import PickleError
import sys
import struct
from functools import partial
from typing import (
    Callable,
    List,
    Optional,
    TypedDict,
    TYPE_CHECKING,
)
import tempfile
import os
import importlib.util
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor
from subprocess import run
import logging

from tqdm import tqdm
import pandas as pd
from google.protobuf.message import Message
import pyarrow
import pyarrow.flight
from pyarrow.flight import FlightDescriptor
from turboml.common.concurrent import multiprocessing_enabled, get_executor_pool_class
from .api import api
from .env import CONFIG
from .internal import TbItertools, TbPyArrow

if TYPE_CHECKING:
    from types import ModuleType
    from .models import (
        RegisteredSchema,
    )
    from google.protobuf import message


logger = logging.getLogger(__name__)


class StreamType(StrEnum):
    INPUT_TOPIC = "input_topic"
    OUTPUT = "output"
    TARGET_DRIFT = "target_drift"
    UNIVARIATE_DRIFT = "univariate_drift"
    MULTIVARIATE_DRIFT = "multivariate_drift"


class Record(TypedDict):
    offset: int
    record: bytes


def _get_raw_msgs(dataset_type: StreamType, name: str, **kwargs):
    """
    Returns a dataframe of type [offset: int, record: bytes] for the dataset
    """
    if dataset_type == StreamType.UNIVARIATE_DRIFT:
        numeric_feature = kwargs.get("numeric_feature")
        if numeric_feature is None:
            raise ValueError("numeric_feature is required for univariate drift")
        name = f"{name}:{numeric_feature}"
    if dataset_type == StreamType.MULTIVARIATE_DRIFT:
        label = kwargs.get("label")
        if label is None:
            raise ValueError("label is required for multivariate drift")
        name = f"{name}:{label}"
    arrow_descriptor = pyarrow.flight.Ticket(f"{dataset_type.value}:{name}")
    client = pyarrow.flight.connect(f"{CONFIG.ARROW_SERVER_ADDRESS}")
    TbPyArrow.wait_for_available(client)
    reader = client.do_get(
        arrow_descriptor,
        options=pyarrow.flight.FlightCallOptions(headers=api.arrow_headers),
    )
    LOG_FREQUENCY_SEC = 3
    last_log_time = 0
    yielded_total = 0
    yielded_batches = 0
    start_time = datetime.now().timestamp()
    while True:
        table = reader.read_chunk().data
        df = TbPyArrow.arrow_table_to_pandas(table)
        if df.empty:
            logger.info(
                f"Yielded {yielded_total} records ({yielded_batches} batches) in {datetime.now().timestamp() - start_time:.0f} seconds"
            )
            break
        yielded_total += len(df)
        yielded_batches += 1
        if (now := datetime.now().timestamp()) - last_log_time > LOG_FREQUENCY_SEC:
            logger.info(
                f"Yielded {yielded_total} records ({yielded_batches} batches) in {now - start_time:.0f} seconds"
            )
            last_log_time = now
        assert isinstance(df, pd.DataFrame)
        yield df


PROTO_PREFIX_BYTE_LEN = 6


def _records_to_proto_messages(
    df: pd.DataFrame,
    proto_msg: Callable[[], message.Message],
) -> tuple[list[int], list[message.Message]]:
    offsets = []
    proto_records = []
    for _, offset_message in df.iterrows():
        offset, message = offset_message["offset"], offset_message["record"]
        assert isinstance(message, bytes)
        proto = proto_msg()
        proto.ParseFromString(message[PROTO_PREFIX_BYTE_LEN:])
        offsets.append(offset)
        proto_records.append(proto)
    return offsets, proto_records


class RecordList(TypedDict):
    offsets: list[int]
    records: list[message.Message]


# HACK: Since it is observed that the ProcessPoolExecutor fails to pickle proto messages under
# certain (not yet understood) conditions, we switch to the ThreadPoolExecutor upon encountering
# such an error.
# Ref: https://turboml.slack.com/archives/C07FM09V0MA/p1729082597265189


def get_proto_msgs(
    dataset_type: StreamType,
    name: str,
    proto_msg: Callable[[], message.Message],
    **kwargs,
    # limit: int = -1
) -> list[Record]:
    executor_pool_class = get_executor_pool_class()
    try:
        return _get_proto_msgs(
            dataset_type, name, proto_msg, executor_pool_class, **kwargs
        )
    except PickleError as e:
        if not multiprocessing_enabled():
            raise e
        logger.warning(
            f"Failed to pickle proto message class {proto_msg}: {e!r}. Retrying with ThreadPoolExecutor"
        )

        return _get_proto_msgs(
            dataset_type, name, proto_msg, ThreadPoolExecutor, **kwargs
        )


def _get_proto_msgs(
    dataset_type: StreamType,
    name: str,
    proto_msg: Callable[[], message.Message],
    executor_cls: type[ProcessPoolExecutor | ThreadPoolExecutor],
    **kwargs,
) -> list[Record]:
    messages_generator = _get_raw_msgs(dataset_type, name, **kwargs)
    offsets = []
    records = []
    with executor_cls(max_workers=os.cpu_count()) as executor:
        futures: list[Future[tuple[list[int], list[message.Message]]]] = []
        for df in messages_generator:
            future = executor.submit(
                _records_to_proto_messages,
                df,
                proto_msg,
            )
            futures.append(future)
        for future in futures:
            offsets_chunk, records_chunk = future.result()
            offsets.extend(offsets_chunk)
            records.extend(records_chunk)

    ret = []
    for i, record in zip(offsets, records, strict=True):
        ret.append({"offset": i, "record": record})
    return ret


def create_protobuf_from_row_tuple(
    row: tuple,
    fields: List[str],
    proto_cls: Callable[[], message.Message],
    prefix: bytes,
):
    """Create a Protocol Buffers (protobuf) message by populating its fields with values from a tuple of row data.

    Args:
        row (Iterable): An iterable representing a row of data. Each element corresponds to a field in the protobuf message.
        fields (List[str]): A list of field names corresponding to the fields in the protobuf message class.
        proto_cls (type): The protobuf message class to instantiate.
        prefix (str): A string prefix to be concatenated with the serialized message.

    Returns:
        str: A string representing the serialized protobuf message with the specified prefix.
    """
    import pandas as pd

    my_msg = proto_cls()
    for i, field in enumerate(fields):
        value = row[i]

        if pd.isna(value):
            # Leave the field unset if the value is NaN
            continue

        try:
            setattr(my_msg, field, value)
        except TypeError as e:
            logger.error(
                f"Error setting field '{field}' with value '{value}' in '{row}': {e!r}"
            )
            raise

    return prefix + my_msg.SerializeToString()


def create_protobuf_from_row_dict(
    row: dict,
    proto_cls: type[message.Message],
    prefix: bytes,
):
    """Create a Protocol Buffers (protobuf) message by populating its fields with values a from dictionary row of data.

    Args:
        row (Iterable): An iterable representing a row of data. Each element corresponds to a field in the protobuf message.
        proto_cls (type): The protobuf message class to instantiate.
        prefix (str): A string prefix to be concatenated with the serialized message.

    Returns:
        str: A string representing the serialized protobuf message with the specified prefix.
    """
    my_msg = proto_cls()
    for field, value in row.items():
        if value is None:
            continue  # skip None values -- protobuf isn't happy with them
        try:
            setattr(my_msg, field, value)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Error setting field '{field}'='{value}': {e!r}") from e

    return prefix + my_msg.SerializeToString()


def _get_message_cls_from_pb_module(
    module: ModuleType, message_name: str | None
) -> type[Message] | None:
    messageClasses = [
        v
        for v in vars(module).values()
        if isinstance(v, type) and issubclass(v, Message)
    ]
    if len(messageClasses) == 0:
        logger.error(
            f"No message classes found in protobuf module composed of classes: {list(vars(module).keys())}"
        )
        return None

    if message_name is None:
        return messageClasses[0] if len(messageClasses) > 0 else None

    matching_class = [v for v in messageClasses if v.DESCRIPTOR.name == message_name]
    if len(matching_class) == 0:
        all_message_names = [v.DESCRIPTOR.name for v in messageClasses]
        logger.error(
            f"Could not find message class '{message_name}' in protobuf module composed of classes: {all_message_names}"
        )
        return None
    return matching_class[0]


def _canonicalize_schema_body(schema_body: str) -> str:
    "Schema registry formats does itd own canonicalization, but we need to do it for comparison"
    return "\n".join(
        line.strip()  # Remove leading/trailing whitespace
        for line in schema_body.split("\n")
        if (
            not line.strip().startswith("//")  # Remove comments
            and not line.strip() == ""
        )  # Remove empty lines
    )


def get_protobuf_class(
    schema: str, message_name: str | None, retry: bool = True
) -> type[Message] | None:
    """
    Generate a python class from a Protocol Buffers (protobuf) schema and message name.
    If class_name is None, the first class in the schema is returned.
    If a matching class is not found, None is returned.
    """
    schema = _canonicalize_schema_body(schema)
    basename = f"p_{hashlib.md5(schema.encode()).hexdigest()[:8]}"
    module_name = f"{basename}_pb2"

    if module_name in sys.modules:
        module = sys.modules[module_name]
        return _get_message_cls_from_pb_module(module, message_name)

    with tempfile.TemporaryDirectory(prefix="turboml_") as tempdir:
        filename = os.path.join(tempdir, f"{basename}.proto")
        with open(filename, "w") as f:
            _ = f.write(schema)
        dirname = os.path.dirname(filename)
        basename = os.path.basename(filename)
        run(
            [
                "protoc",
                f"--python_out={dirname}",
                f"--proto_path={dirname}",
                basename,
            ],
            check=True,
        )
        module_path = os.path.join(dirname, module_name + ".py")
        module_spec = importlib.util.spec_from_file_location(module_name, module_path)
        assert module_spec is not None
        assert module_spec.loader is not None
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        if _get_message_cls_from_pb_module(module, None) is None:
            # Retry once if the module is empty
            # This is a rather bizarre behavior that seems to occur
            # in our CI, so we retry once to see if it resolves itself
            if not retry:
                return None
            logger.error(
                f"A seemingly empty protobuf module was generated from module_path='{module_path}', schema={schema}. Retrying once..."
            )
            return get_protobuf_class(schema, message_name, retry=False)

        sys.modules[module_name] = module
        return _get_message_cls_from_pb_module(module, message_name)


def upload_df(
    dataset_id: str,
    df: pd.DataFrame,
    schema: RegisteredSchema,
    protoMessageClass: Optional[type[message.Message]] = None,
) -> None:
    """Upload data from a DataFrame to a dataset after preparing and serializing it as Protocol Buffers (protobuf) messages.

    Args:
        dataset_id (str): The Kafka dataset_id to which the data will be sent.
        df (pd.DataFrame): The DataFrame containing the data to be uploaded.
        schema (Schema): Dataset schema.
        protoMessageClass (Optional(Message)): Protobuf Message Class to use. Generated if not provided.
    """
    # dataset = api.get(f"dataset?dataset_id={dataset_id}").json()
    # dataset = Dataset(**dataset)
    if protoMessageClass is None:
        protoMessageClass = get_protobuf_class(
            schema=schema.schema_body, message_name=schema.message_name
        )
        if protoMessageClass is None:
            raise ValueError(
                f"Could not find protobuf message class message={schema.message_name} schema={schema.schema_body}"
            )

    fields = df.columns.tolist()
    prefix = struct.pack("!xIx", schema.id)
    descriptor = FlightDescriptor.for_command(f"produce:{dataset_id}")
    pa_schema = pyarrow.schema([("value", pyarrow.binary())])

    partial_converter_func = partial(
        create_protobuf_from_row_tuple,
        fields=fields,
        proto_cls=protoMessageClass,
        prefix=prefix,
    )

    logger.info(f"Uploading {df.shape[0]} rows to dataset {dataset_id}")
    executor_pool_class = get_executor_pool_class()

    client = pyarrow.flight.connect(f"{CONFIG.ARROW_SERVER_ADDRESS}")
    TbPyArrow.wait_for_available(client)
    writer, _ = client.do_put(
        descriptor,
        pa_schema,
        options=pyarrow.flight.FlightCallOptions(headers=api.arrow_headers),
    )
    try:
        _upload_df_batch(df, executor_pool_class, partial_converter_func, writer)
    except (PickleError, ModuleNotFoundError) as e:
        if not multiprocessing_enabled():
            raise e
        logger.warning(
            f"Dataframe batch update failed due to exception {e!r}. Retrying with ThreadPoolExecutor"
        )
        _upload_df_batch(df, ThreadPoolExecutor, partial_converter_func, writer)

    logger.info("Upload complete. Waiting for server to process messages.")
    writer.close()


def _upload_df_batch(
    df: pd.DataFrame,
    executor_pool_class: type[ProcessPoolExecutor | ThreadPoolExecutor],
    partial_func,
    writer,
):
    with executor_pool_class(max_workers=os.cpu_count()) as executor:
        data_iterator = executor.map(
            partial_func,
            df.itertuples(index=False, name=None),
            chunksize=1024,
        )

        CHUNK_SIZE = 1024
        row_length = df.shape[0]
        with tqdm(
            total=row_length, desc="Progress", unit="rows", unit_scale=True
        ) as pbar:
            for messages in TbItertools.chunked(data_iterator, CHUNK_SIZE):
                batch = pyarrow.RecordBatch.from_arrays([messages], ["value"])
                writer.write(batch)
                pbar.update(len(messages))
