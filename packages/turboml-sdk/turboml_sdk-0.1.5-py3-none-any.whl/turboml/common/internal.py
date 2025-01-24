import itertools
from typing import Generator, Iterable
import typing
from pandas.core.base import DtypeObj
import pyarrow as pa
import pyarrow.flight
import pandas as pd
import logging
import threading

from .api import api
from tqdm import tqdm

from .models import InputSpec

logger = logging.getLogger(__name__)


class TurboMLResourceException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class TbPyArrow:
    """
    Utility class containing some shared methods and data for our
    PyArrow based data exchange.
    """

    @staticmethod
    def _input_schema(has_labels: bool) -> pa.Schema:
        label_schema = [("label", pa.float32())] if has_labels else []
        return pa.schema(
            [
                ("numeric", pa.list_(pa.float32())),
                ("categ", pa.list_(pa.int64())),
                ("text", pa.list_(pa.string())),
                ("image", pa.list_(pa.binary())),
                ("time_tick", pa.int32()),
                ("key", pa.string()),
            ]
            + label_schema
        )

    @staticmethod
    def arrow_table_to_pandas(
        table: pa.Table, to_pandas_opts: dict | None = None
    ) -> pd.DataFrame:
        default_opts = {"split_blocks": False, "date_as_object": False}
        to_pandas_opts = {**default_opts, **(to_pandas_opts or {})}
        return table.to_pandas(**to_pandas_opts)

    @staticmethod
    def df_to_table(df: pd.DataFrame, input_spec: InputSpec) -> pa.Table:
        # transform df to input form, where each column
        # is a list of values of the corresponding type
        input_df = pd.DataFrame()
        input_df["key"] = df[input_spec.key_field].astype("str").values
        input_df["time_tick"] = (
            0
            if input_spec.time_field in ["", None]
            else df[input_spec.time_field].astype("int32").values
        )
        input_df["numeric"] = (
            df[input_spec.numerical_fields].astype("float32").values.tolist()
        )
        input_df["categ"] = (
            df[input_spec.categorical_fields].astype("int64").values.tolist()
        )
        input_df["text"] = df[input_spec.textual_fields].astype("str").values.tolist()
        input_df["image"] = (
            df[input_spec.imaginal_fields].astype("bytes").values.tolist()
        )

        has_labels = input_spec.label_field is not None and input_spec.label_field in df
        if has_labels:
            input_df["label"] = df[input_spec.label_field].astype("float32").values

        return pa.Table.from_pandas(input_df, TbPyArrow._input_schema(has_labels))

    @staticmethod
    def wait_for_available(client: pyarrow.flight.FlightClient, timeout=10):
        try:
            client.wait_for_available(timeout=timeout)
        except pyarrow.flight.FlightUnauthenticatedError:
            # Server is up - wait_for_available() does not ignore auth errors
            pass

    @staticmethod
    def handle_flight_error(
        e: Exception, client: pyarrow.flight.FlightClient, allow_recovery=True
    ):
        if isinstance(e, pyarrow.flight.FlightUnavailableError):
            if not allow_recovery:
                raise TurboMLResourceException(
                    "Failed to initialize TurboMLArrowServer: Check logs for more details"
                ) from e

            # If the server is not available, we can try to start it
            api.post(endpoint="start_arrow_server")
            TbPyArrow.wait_for_available(client)
            return
        if isinstance(e, pyarrow.flight.FlightTimedOutError):
            if not allow_recovery:
                raise TurboMLResourceException(
                    "Flight server timed out: Check logs for more details"
                ) from e
            TbPyArrow.wait_for_available(client)
            return
        if isinstance(e, pyarrow.flight.FlightInternalError):
            raise TurboMLResourceException(
                f"Internal flight error: {e!r}. Check logs for more details"
            ) from e
        if isinstance(e, pyarrow.flight.FlightError):
            raise TurboMLResourceException(
                f"Flight server error: {e!r}. Check logs for more details"
            ) from e
        raise Exception(f"Unknown error: {e!r}") from e

    @staticmethod
    def _put_and_retry(
        client: pyarrow.flight.FlightClient,
        upload_descriptor: pyarrow.flight.FlightDescriptor,
        options: pyarrow.flight.FlightCallOptions,
        input_table: pa.Table,
        can_retry: bool = True,
        max_chunksize: int = 1024,
        epochs: int = 1,
    ) -> None:
        try:
            writer, _ = client.do_put(
                upload_descriptor, input_table.schema, options=options
            )
            TbPyArrow._write_in_chunks(
                writer, input_table, max_chunksize=max_chunksize, epochs=epochs
            )
            writer.close()
        except Exception as e:
            TbPyArrow.handle_flight_error(e, client, can_retry)
            return TbPyArrow._put_and_retry(
                client,
                upload_descriptor,
                options,
                input_table,
                can_retry=False,
                max_chunksize=max_chunksize,
                epochs=epochs,
            )

    @staticmethod
    def _exchange_and_retry(
        client: pyarrow.flight.FlightClient,
        upload_descriptor: pyarrow.flight.FlightDescriptor,
        options: pyarrow.flight.FlightCallOptions,
        input_table: pa.Table,
        can_retry: bool = True,
        max_chunksize: int = 1024,
    ) -> pa.Table:
        try:
            writer, reader = client.do_exchange(upload_descriptor, options=options)
            writer.begin(input_table.schema)
            write_event = threading.Event()
            writer_thread = threading.Thread(
                target=TbPyArrow._write_in_chunks,
                args=(writer, input_table),
                kwargs={
                    "max_chunksize": max_chunksize,
                    "write_event": write_event,
                },
            )
            writer_thread.start()
            write_event.wait()
            read_result = TbPyArrow._read_in_chunks(reader)
            writer_thread.join()
            writer.close()
            return read_result
        except Exception as e:
            TbPyArrow.handle_flight_error(e, client, can_retry)
            return TbPyArrow._exchange_and_retry(
                client,
                upload_descriptor,
                options,
                input_table,
                can_retry=False,
                max_chunksize=max_chunksize,
            )

    @staticmethod
    def _write_in_chunks(
        writer: pyarrow.flight.FlightStreamWriter,
        input_table: pa.Table,
        write_event: threading.Event | None = None,
        max_chunksize: int = 1024,
        epochs: int = 1,
    ) -> None:
        total_rows = input_table.num_rows
        n_chunks = total_rows // max_chunksize + 1
        logger.info(f"Starting to upload data... Total rows: {total_rows}")

        for epoch in range(epochs):
            with tqdm(
                total=n_chunks, desc="Progress", unit="chunk", unit_scale=True
            ) as pbar:
                if epochs > 1:
                    pbar.set_postfix(epoch=epoch + 1)

                for start in range(0, total_rows, max_chunksize):
                    chunk_table = input_table.slice(
                        start, min(max_chunksize, total_rows - start)
                    )
                    writer.write_table(chunk_table)
                    if start == 0 and write_event:
                        write_event.set()
                    pbar.update(1)

        writer.done_writing()
        logger.info("Completed data upload.")

    @staticmethod
    def _read_in_chunks(reader: pyarrow.flight.FlightStreamReader) -> pa.Table:
        batches = []
        while True:
            try:
                chunk = reader.read_chunk()
                batches.append(chunk.data)
            except StopIteration:
                break
        return pa.Table.from_batches(batches) if batches else None


class TbPandas:
    @staticmethod
    def fill_nans_with_default(series: pd.Series):
        if series.isna().any():
            default = TbPandas.default_for_type(series.dtype)
            return series.fillna(value=default)
        return series

    @staticmethod
    def default_for_type(dtype: DtypeObj):
        if pd.api.types.is_numeric_dtype(dtype):
            return 0
        if pd.api.types.is_string_dtype(dtype):
            return ""
        if pd.api.types.is_bool_dtype(dtype):
            return False
        if pd.api.types.is_datetime64_dtype(dtype):
            return pd.Timestamp("1970-01-01")
        raise ValueError(f"Unsupported dtype: {dtype}")


T = typing.TypeVar("T")


class TbItertools:
    @staticmethod
    def chunked(iterable: Iterable[T], n: int) -> Generator[list[T], None, None]:
        """Yield successive n-sized chunks from iterable."""
        iterator = iter(iterable)
        while True:
            chunk = list(itertools.islice(iterator, n))
            if not chunk:
                break
            yield list(chunk)
