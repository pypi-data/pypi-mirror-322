from __future__ import annotations
from copy import deepcopy
import re
from typing import (
    Any,
    Optional,
    Tuple,
    Literal,
    Type,
    List,
    Union,
    Annotated,
    TYPE_CHECKING,
)
from enum import StrEnum, Enum, auto
from datetime import datetime, timezone

from google.protobuf.descriptor import FieldDescriptor
from pydantic import (
    Base64Bytes,
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    StringConstraints,
    create_model,
    field_serializer,
    field_validator,
    validator,
    model_validator,
    StrictBool,
)
from pandas._libs.tslibs.timestamps import Timestamp
import pandas as pd
import numpy as np

from turboml.common import dataloader


from .sources import PostgresSource, FileSource  # noqa: TCH001

if TYPE_CHECKING:
    from pydantic.fields import FieldInfo


TurboMLResourceIdentifier = Annotated[
    str,
    StringConstraints(
        pattern=r"^[a-zA-Z0-9_-]+$",
        # TODO: We need to ensure we're using this type everywhere identifiers are accepted (url/query params!)
        # Otherwise this would break APIs.
        # to_lower=True,
    ),
]
DatasetId = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$")]

# Since our dataset fields are used as protobuf message fields, we need to ensure they're valid
# protobuf field names. This means they must start with an underscore ('_') or a letter (a-z, A-Z),
# followed by alphanumeric characters or underscores.
DatasetField = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$")]

SQLIden = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$")]


class SchemaType(StrEnum):
    PROTOBUF = "PROTOBUF"


class KafkaConnectDatasetRegistrationRequest(BaseModel):
    dataset_id: DatasetId
    source: Union[FileSource, PostgresSource]
    key_field: str

    @field_validator("dataset_id")
    def check_dataset_id(cls, v: str):
        # We use `.` to partition dataset_ids into namespaces, so we don't allow it in dataset names
        # `-` is used as another internal delimiter, so we don't allow it either.
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Invalid dataset name")
        return v


class Datatype(StrEnum):
    """
    Data types supported by the TurboML platform, corresponding to protobuf types.
    """

    INT32 = auto()
    INT64 = auto()
    FLOAT = auto()
    DOUBLE = auto()
    STRING = auto()
    BOOL = auto()
    BYTES = auto()

    # TODO: we support some more types for floats and datetimes...

    def to_protobuf_type(self) -> str:
        return str(self).lower()

    @staticmethod
    def from_proto_field_descriptor_type(type_: int) -> Datatype:
        match type_:
            case FieldDescriptor.TYPE_INT32:
                return Datatype.INT32
            case FieldDescriptor.TYPE_INT64:
                return Datatype.INT64
            case FieldDescriptor.TYPE_FLOAT:
                return Datatype.FLOAT
            case FieldDescriptor.TYPE_DOUBLE:
                return Datatype.DOUBLE
            case FieldDescriptor.TYPE_STRING:
                return Datatype.STRING
            case FieldDescriptor.TYPE_BOOL:
                return Datatype.BOOL
            case FieldDescriptor.TYPE_BYTES:
                return Datatype.BYTES
            case _:
                raise ValueError(f"Unsupported protobuf type: {type_}")

    def to_pandas_dtype(self) -> str:
        """Convert TurboML datatype to pandas dtype that works with astype()"""
        match self:
            case Datatype.INT32:
                return "int32"
            case Datatype.INT64:
                return "int64"
            case Datatype.FLOAT:
                return "float32"
            case Datatype.DOUBLE:
                return "float64"
            case Datatype.STRING:
                return "string"
            case Datatype.BOOL:
                return "bool"
            case Datatype.BYTES:
                return "bytes"
            case _:
                raise ValueError(f"Unsupported datatype for pandas conversion: {self}")

    @staticmethod
    def from_pandas_column(column: pd.Series) -> Datatype:
        match column.dtype:
            case np.int32:
                return Datatype.INT32
            case np.int64:
                return Datatype.INT64
            case np.float32:
                return Datatype.FLOAT
            case np.float64:
                return Datatype.DOUBLE
            case np.bool_:
                return Datatype.BOOL
            case np.bytes_:
                return Datatype.BYTES
            case "string":
                return Datatype.STRING
            case np.object_:
                # At this point we're not sure of the type: pandas by default
                # interprets both `bytes` and `str` into `object_` columns
                proto_dtype = Datatype._infer_pd_object_col_type(column)
                if proto_dtype is None:
                    raise ValueError(f"Unsupported dtype: {column.dtype}")
                return proto_dtype
            case _:
                raise ValueError(f"Unsupported dtype: {column.dtype}")

    @staticmethod
    def _infer_pd_object_col_type(column: pd.Series) -> Optional[Datatype]:
        first_non_na_idx = column.first_valid_index()
        if first_non_na_idx is None:
            return None
        try:
            if (
                isinstance(column.loc[first_non_na_idx], str)
                and column.astype(str) is not None
            ):
                return Datatype.STRING
        except UnicodeDecodeError:
            pass

        try:
            if (
                isinstance(column.loc[first_non_na_idx], bytes)
                and column.astype(bytes) is not None
            ):
                return Datatype.BYTES
        except TypeError:
            pass

        return None


class DatasetSchema(BaseModel):
    fields: dict[TurboMLResourceIdentifier, Datatype]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{k}: {v}' for k, v in self.fields.items())})"

    @staticmethod
    def from_pd(df: pd.DataFrame) -> DatasetSchema:
        fields = {}
        for column_name in df.columns:
            column = df[column_name]
            assert isinstance(column, pd.Series)
            fields[column_name] = Datatype.from_pandas_column(column)
        return DatasetSchema(fields=fields)

    @staticmethod
    def from_protobuf_schema(schema: str, message_name: str | None) -> DatasetSchema:
        cls = dataloader.get_protobuf_class(
            schema=schema,
            message_name=message_name,
        )
        if cls is None:
            raise ValueError(
                f"No matching protobuf message found for message={message_name}, schema={schema}"
            )
        columns = {}
        for field in cls.DESCRIPTOR.fields:
            name = field.name
            proto_type = Datatype.from_proto_field_descriptor_type(field.type)
            columns[name] = proto_type
        return DatasetSchema(fields=columns)

    def to_protobuf_schema(self, message_name: str) -> str:
        NEWLINE = "\n"

        def column_to_field_decl(cname: str, ctype: Datatype, idx: int) -> str:
            return f"optional {ctype.to_protobuf_type()} {cname} = {idx};"

        field_decls = map(
            column_to_field_decl,
            self.fields.keys(),
            self.fields.values(),
            range(1, len(self.fields) + 1),
        )
        return f"""
syntax = "proto2";
message {message_name} {{
{NEWLINE.join(field_decls)}
}}
"""


class DatasetRegistrationRequest(BaseModel):
    class SchemaFromRegistry(BaseModel):
        type_: Literal["registry"] = "registry"
        kind: Literal["protobuf"] = "protobuf"
        message_name: str

    class ExplicitSchema(DatasetSchema):
        type_: Literal["explicit"] = "explicit"

        @staticmethod
        def from_pd(df: pd.DataFrame) -> DatasetRegistrationRequest.ExplicitSchema:
            ds = DatasetSchema.from_pd(df)
            return DatasetRegistrationRequest.ExplicitSchema(**ds.model_dump())

    dataset_id: DatasetId
    data_schema: Union[SchemaFromRegistry, ExplicitSchema] = Field(
        discriminator="type_"
    )
    key_field: str


class RegisteredSchema(BaseModel):
    id: int
    schema_type: SchemaType
    schema_body: str
    message_name: str
    native_schema: DatasetSchema


class DatasetRegistrationResponse(BaseModel):
    registered_schema: RegisteredSchema


class DatasetSpec(BaseModel):
    dataset_id: DatasetId
    key: str


class DbColumn(BaseModel):
    name: str
    dtype: str


class Dataset(BaseModel):
    class JoinInformation(BaseModel):
        sources: tuple[DatasetId, DatasetId]
        joined_on_column_pairs: list[tuple[str, str]]
        prefixes: tuple[SQLIden, SQLIden]

    class Metadata(BaseModel):
        kafka_topic: str
        input_pb_message_name: str
        risingwave_source: str
        risingwave_view: str
        join_information: Optional[Dataset.JoinInformation] = None

    feature_version: int = 0
    sink_version: int = 0
    table_columns: list[DbColumn]
    key: str
    source_type: str
    message_name: str
    file_proto: str
    sql_feats: dict[str, dict] = Field(default_factory=dict)  # TODO: type
    agg_feats: dict[str, dict] = Field(default_factory=dict)  # TODO: type
    udf_feats: dict[str, dict] = Field(default_factory=dict)  # TODO: type
    udaf_feats: dict[str, dict] = Field(default_factory=dict)  # TODO: type
    agg_cols_indexes: list[str] = Field(default_factory=list)
    meta: Metadata = Field()
    timestamp_fields: dict[str, str] = Field(default_factory=dict)
    drifts: list[DataDrift] = Field(default_factory=list)
    ibis_feats: list[dict] = Field(default_factory=list)


class LabelAssociation(BaseModel):
    dataset_id: DatasetId
    field: str


class LearnerConfig(BaseModel):
    predict_workers: int
    update_batch_size: int
    synchronization_method: str


class ModelParams(BaseModel):
    # Silence pydantic warning about protected namespace
    model_config = ConfigDict(protected_namespaces=())

    model_configs: list[dict]

    # TODO: We should replace these with InputSpec
    label: LabelAssociation
    numerical_fields: list[str]
    categorical_fields: list[str]
    textual_fields: list[str]
    imaginal_fields: list[str]
    time_field: Optional[str]


class MLModellingRequest(ModelParams):
    id: TurboMLResourceIdentifier
    dataset_id: DatasetId

    # Use a pretrained model as the initial state
    initial_model_id: Optional[str] = None

    learner_config: Optional[LearnerConfig] = None
    predict_only: bool = False


class ModelConfigStorageRequest(BaseModel):
    id: TurboMLResourceIdentifier
    version: TurboMLResourceIdentifier
    initial_model_key: str | None
    params: ModelParams | None

    @model_validator(mode="after")
    def validate_model_params(self):
        if not self.initial_model_key and not self.params:
            raise ValueError(
                "Either initial_model_key or model_params must be provided"
            )
        return self


class DataDriftType(StrEnum):
    UNIVARIATE = "univariate"
    MULTIVARIATE = "multivariate"


class DataDrift(BaseModel):
    label: Optional[TurboMLResourceIdentifier]
    numerical_fields: list[str]

    # TODO: we could do some validations on fields for improved UX
    # (verify that they're present and are numeric)


class DriftQuery(BaseModel):
    limit: int = 100
    start_timestamp: datetime
    end_timestamp: datetime


class DataDriftQuery(DataDrift, DriftQuery):
    pass


class TargetDriftQuery(DriftQuery):
    pass


class DriftScores(BaseModel):
    scores: List[float]
    timestamps: List[int]

    @validator("timestamps", pre=True, each_item=True)
    def convert_timestamp_to_epoch_microseconds(
        cls, value: Union[Timestamp, Any]
    ) -> int:
        if isinstance(value, Timestamp):
            return int(value.timestamp() * 1_000_000)
        return int(float(value) * 1_000_000)


class VenvSpec(BaseModel):
    venv_name: str
    lib_list: list[str]

    @field_validator("venv_name")
    def ensure_venv_name_is_not_funny(cls, v):
        # Restrict venv names to alphanumeric
        safe_name_regex = r"^[a-zA-Z0-9_]+$"
        if not re.match(safe_name_regex, v):
            raise ValueError("Venv name must be alphanumeric")
        return v


class AddPythonClassRequest(BaseModel):
    class PythonClassValidationType(StrEnum):
        NONE = auto()
        MODEL_CLASS = auto()
        MODULE = auto()

    obj: Base64Bytes
    name: str
    # NOTE: No validations on the backend for now
    validation_type: Optional[PythonClassValidationType] = (
        PythonClassValidationType.NONE
    )


class HFToGGUFRequest(BaseModel):
    class GGUFType(StrEnum):
        F32 = "f32"
        F16 = "f16"
        BF16 = "bf16"
        QUANTIZED_8_0 = "q8_0"
        AUTO = "auto"

    hf_repo_id: str
    model_type: GGUFType = Field(default=GGUFType.AUTO)
    select_gguf_file: Optional[str] = None

    @field_validator("hf_repo_id")
    def validate_hf_repo_id(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]+\/[a-zA-Z0-9_\.-]+$", v):
            raise ValueError("Invalid HF repo id")
        return v

    class Config:
        protected_namespaces = ()


class ModelAcquisitionJob(BaseModel):
    class AcquisitionStatus(StrEnum):
        PENDING = "pending"
        IN_PROGRESS = "in_progress"
        COMPLETED = "completed"
        FAILED = "failed"

    job_id: str
    status: AcquisitionStatus = AcquisitionStatus.PENDING
    hf_repo_id: str
    model_type: str
    select_gguf_file: Optional[str] = None
    gguf_id: Optional[str] = None
    error_message: Optional[str] = None
    progress_message: Optional[str] = None


class LlamaServerRequest(BaseModel):
    class SourceType(StrEnum):
        HUGGINGFACE = "huggingface"
        GGUF_ID = "gguf_id"

    class HuggingFaceSpec(HFToGGUFRequest):
        pass

    class ServerParams(BaseModel):
        threads: int = -1
        seed: int = -1
        context_size: int = 0
        flash_attention: bool = False

    source_type: SourceType
    gguf_id: Optional[str] = None
    hf_spec: Optional[HuggingFaceSpec] = None
    server_params: ServerParams = Field(default_factory=ServerParams)

    @field_validator("source_type", mode="before")
    def accept_string_for_enum(cls, v):
        if isinstance(v, str):
            return cls.SourceType(v)
        return v

    @model_validator(mode="after")
    def validate_model_source(self):
        if self.source_type == self.SourceType.HUGGINGFACE and not self.hf_spec:
            raise ValueError("Huggingface model source requires hf_spec")
        if self.source_type == self.SourceType.GGUF_ID and not self.gguf_id:
            raise ValueError("GGUF model source requires gguf_id")
        return self


class LlamaServerResponse(BaseModel):
    server_id: str
    server_relative_url: str


class HFToGGUFResponse(BaseModel):
    gguf_id: str


class MetricRegistrationRequest(BaseModel):
    # TODO: metric types should be enum (incl custom metrics)
    metric: str


class FeatureMetadata(BaseModel):
    author: int
    introduced_in_version: int
    created_at: str  # As datetime is not json serializable
    datatype: str  # Pandas type as SDK is python


class SqlFeatureSpec(BaseModel):
    feature_name: str
    sql_spec: str


class AggregateFeatureSpec(BaseModel):
    feature_name: str
    column: str
    aggregation_function: str
    group_by_columns: list[str]
    interval: str
    timestamp_column: str


class UdafFeatureSpec(BaseModel):
    feature_name: str
    arguments: list[str]
    function_name: str
    group_by_columns: list[str]
    timestamp_column: str
    interval: str


class CustomMetric(BaseModel):
    metric_name: str
    metric_spec: dict


class RwEmbeddedUdafFunctionSpec(BaseModel):
    input_types: list[str]
    output_type: str
    function_file_contents: str


class ExternalUdafFunctionSpec(BaseModel):
    obj: Base64Bytes


class UdafFunctionSpec(BaseModel):
    name: Annotated[
        str, StringConstraints(min_length=1, pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$")
    ]
    libraries: list[str]
    spec: RwEmbeddedUdafFunctionSpec | ExternalUdafFunctionSpec


class UdfFeatureSpec(BaseModel):
    feature_name: str
    arguments: list[str]
    function_name: str
    libraries: list[str]
    is_rich_function: bool = False
    io_threads: Optional[int] = None
    class_name: Optional[str] = None
    initializer_arguments: list[str]


class UdfFunctionSpec(BaseModel):
    name: Annotated[
        str, StringConstraints(min_length=1, pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$")
    ]
    input_types: list[str]
    output_type: str
    libraries: list[str]
    function_file_contents: str
    is_rich_function: bool = False
    io_threads: Optional[int] = None
    class_name: Optional[str] = None
    initializer_arguments: list[str]

    @model_validator(mode="after")
    def validate_rich_function(self):
        if self.is_rich_function and not self.class_name:
            raise ValueError("class_name is required for rich functions")
        return self


class IbisFeatureSpec(BaseModel):
    dataset_id: DatasetId
    udfs_spec: list[UdfFunctionSpec]
    encoded_table: str


class FeatureGroup(BaseModel):
    feature_version: int = 0
    key_field: str
    meta: dict = Field(default_factory=dict)
    udfs_spec: list[UdfFunctionSpec]
    primary_source_name: str


class BackEnd(Enum):
    Risingwave = auto()
    Flink = auto()


class ApiKey(BaseModel):
    id: int
    "Unique identifier for the key"
    suffix: str
    "Last 8 characters of the key"
    expire_at: Optional[datetime]
    label: Optional[str]
    created_at: datetime
    revoked_at: Optional[datetime]


class FetchFeatureRequest(BaseModel):
    dataset_id: DatasetId
    limit: int


class FeatureMaterializationRequest(BaseModel):
    dataset_id: DatasetId
    sql_feats: list[SqlFeatureSpec] = Field(default_factory=list)
    agg_feats: list[AggregateFeatureSpec] = Field(default_factory=list)
    udf_feats: list[UdfFeatureSpec] = Field(default_factory=list)
    udaf_feats: list[UdafFeatureSpec] = Field(default_factory=list)
    ibis_feats: Optional[IbisFeatureSpec] = None


class FeaturePreviewRequest(FeatureMaterializationRequest):
    limit: int = 10


class IbisFeatureMaterializationRequest(BaseModel):
    feature_group_name: Annotated[
        str,
        StringConstraints(min_length=1, pattern=r"^[a-z]([a-z0-9_]{0,48}[a-z0-9])?$"),
    ]
    key_field: str
    udfs_spec: list[UdfFunctionSpec]
    backend: BackEnd
    encoded_table: str
    primary_source_name: str

    @field_serializer("backend")
    def serialize_backend(self, backend: BackEnd, _info):
        return backend.value


class TimestampQuery(BaseModel):
    column_name: str
    timestamp_format: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class Oauth2StartResponse(BaseModel):
    auth_uri: str


class NewApiKeyRequest(BaseModel):
    expire_at: Optional[datetime]
    label: str

    @field_validator("expire_at")
    def validate_expire_at(cls, v):
        if v is not None and v < datetime.now():
            raise ValueError("expire_at must be in the future")
        return v


class NewApiKeyResponse(BaseModel):
    key: str
    expire_at: Optional[datetime]


def _partial_model(model: Type[BaseModel]):
    """
    Decorator to create a partial model, where all fields are optional.
    Useful for PATCH requests, where we want to allow partial updates
    and the models may be derived from the original model.
    """

    def make_field_optional(
        field: FieldInfo, default: Any = None
    ) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new

    fields = {
        field_name: make_field_optional(field_info)
        for field_name, field_info in model.model_fields.items()
    }
    return create_model(  # type: ignore
        f"Partial{model.__name__}",
        __doc__=model.__doc__,
        __base__=model,
        __module__=model.__module__,
        **fields,  # type: ignore
    )


@_partial_model
class ApiKeyPatchRequest(BaseModel):
    label: Optional[str]
    expire_at: Optional[datetime]

    @field_validator("expire_at", mode="before")
    def validate_expire_at(cls, v):
        if v is None:
            return None
        v = datetime.fromtimestamp(v, tz=timezone.utc)
        if v < datetime.now(timezone.utc):
            raise ValueError("expire_at must be in the future")
        return v


class User(BaseModel):
    id: int
    username: str
    email: str | None = None


class NamespaceAcquisitionRequest(BaseModel):
    namespace: Annotated[
        str,
        StringConstraints(
            min_length=1, max_length=32, pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$"
        ),
    ]


class UserManager:
    def __init__(self):
        # Cache username -> user
        # TODO: we should change this to user_id -> user, along
        # with changing the API/auth to use user_id instead of username.
        # This is part of our agreement to use username for display purposes only,
        # as well as most of our other resources using IDs.
        self.user_cache = {}


class TosResponse(BaseModel):
    version: int
    format: str  # text/plain or text/html
    content: str


class TosAcceptanceRequest(BaseModel):
    version: int


class InputSpec(BaseModel):
    key_field: str
    time_field: Optional[str]
    numerical_fields: list[str]
    categorical_fields: list[str]
    textual_fields: list[str]
    imaginal_fields: list[str]

    label_field: str


class ModelMetadata(BaseModel):
    # NOTE: We could use a proto-derived pydantic model here
    # (with `so1n/protobuf_to_pydantic`) but on our last attempt
    # the generated models were problematic for `oneof` proto fields and the hacks
    # weren't worth it. We can still revisit this in the future.
    # Ref: https://github.com/so1n/protobuf_to_pydantic/issues/31
    process_config: dict
    offset: str
    input_db_source: str
    input_db_columns: list[DbColumn]
    metrics: list[str]
    label_association: LabelAssociation
    drift: str

    def get_input_spec(self) -> InputSpec:
        key_field = self.process_config["inputConfig"]["keyField"]
        time_field = self.process_config["inputConfig"].get("time_tick", None)
        numerical_fields = list(self.process_config["inputConfig"].get("numerical", []))
        categorical_fields = list(
            self.process_config["inputConfig"].get("categorical", [])
        )
        textual_fields = list(self.process_config["inputConfig"].get("textual", []))
        imaginal_fields = list(self.process_config["inputConfig"].get("imaginal", []))
        # label_field = self.label_association.field if self.label_association else None
        return InputSpec(
            key_field=key_field,
            time_field=time_field,
            numerical_fields=numerical_fields,
            categorical_fields=categorical_fields,
            textual_fields=textual_fields,
            imaginal_fields=imaginal_fields,
            label_field=self.label_association.field,
        )


class ModelInfo(BaseModel):
    metadata: ModelMetadata
    endpoint_paths: list[str]


class StoredModel(BaseModel):
    name: str
    version: str
    stored_size: int
    created_at: datetime


class ProcessMeta(BaseModel):
    caller: str
    namespace: str
    job_id: str


class ProcessInfo(BaseModel):
    pid: int
    cmd: list[str]
    stdout_path: str
    stderr_path: str
    # For turboml jobs
    meta: Optional[ProcessMeta]
    restart: bool
    stopped: bool = False

    @field_validator("cmd", mode="before")
    def tolerate_string_cmd(cls, v):  # For backward compatibility
        if isinstance(v, str):
            return v.split()
        return v


class ProcessOutput(BaseModel):
    stdout: str
    stderr: str


class ProcessPatchRequest(BaseModel):
    action: Literal["kill", "restart"]


class ModelPatchRequest(BaseModel):
    action: Literal["pause", "resume"]


class ModelDeleteRequest(BaseModel):
    delete_output_topic: StrictBool


# Moved from ml_algs
class SupervisedAlgorithms(StrEnum):
    HoeffdingTreeClassifier = "HoeffdingTreeClassifier"
    HoeffdingTreeRegressor = "HoeffdingTreeRegressor"
    AMFClassifier = "AMFClassifier"
    AMFRegressor = "AMFRegressor"
    FFMClassifier = "FFMClassifier"
    FFMRegressor = "FFMRegressor"
    SGTClassifier = "SGTClassifier"
    SGTRegressor = "SGTRegressor"
    SNARIMAX = "SNARIMAX"
    LeveragingBaggingClassifier = "LeveragingBaggingClassifier"
    HeteroLeveragingBaggingClassifier = "HeteroLeveragingBaggingClassifier"
    AdaBoostClassifier = "AdaBoostClassifier"
    HeteroAdaBoostClassifier = "HeteroAdaBoostClassifier"
    RandomSampler = "RandomSampler"
    NeuralNetwork = "NeuralNetwork"
    ONN = "ONN"
    Python = "Python"
    OVR = "OVR"
    BanditModelSelection = "BanditModelSelection"
    ContextualBanditModelSelection = "ContextualBanditModelSelection"
    RandomProjectionEmbedding = "RandomProjectionEmbedding"
    EmbeddingModel = "EmbeddingModel"
    MultinomialNB = "MultinomialNB"
    GaussianNB = "GaussianNB"
    AdaptiveXGBoost = "AdaptiveXGBoost"
    AdaptiveLGBM = "AdaptiveLGBM"
    LLAMAEmbedding = "LLAMAEmbedding"
    LlamaText = "LlamaText"
    RestAPIClient = "RestAPIClient"
    ClipEmbedding = "ClipEmbedding"
    PythonEnsembleModel = "PythonEnsembleModel"
    GRPCClient = "GRPCClient"


class UnsupervisedAlgorithms(StrEnum):
    MStream = "MStream"
    RCF = "RCF"
    HST = "HST"
    ONNX = "ONNX"


class EvaluationMetrics(StrEnum):
    WindowedAUC = "WindowedAUC"
    WindowedMAE = "WindowedMAE"
    WindowedMSE = "WindowedMSE"
    WindowedRMSE = "WindowedRMSE"
    WindowedAccuracy = "WindowedAccuracy"


# Timestamp conversion and support for duckdb and risingwave
class TimestampRealType(StrEnum):
    epoch_seconds = "epoch_seconds"
    epoch_milliseconds = "epoch_milliseconds"


class RisingWaveVarcharType(StrEnum):
    YYYY_MM_DD = "YYYY MM DD"
    YYYY_MM_DD_HH24_MI_SS_US = "YYYY-MM-DD HH24:MI:SS.US"
    YYYY_MM_DD_HH12_MI_SS_US = "YYYY-MM-DD HH12:MI:SS.US"
    YYYY_MM_DD_HH12_MI_SS_MS = "YYYY-MM-DD HH12:MI:SS.MS"
    YYYY_MM_DD_HH24_MI_SS_MS = "YYYY-MM-DD HH24:MI:SS.MS"
    YYYY_MM_DD_HH24_MI_SSTZH_TZM = "YYYY-MM-DD HH24:MI:SSTZH:TZM"
    YYYY_MM_DD_HH12_MI_SSTZH_TZM = "YYYY-MM-DD HH12:MI:SSTZH:TZM"


class DuckDbVarcharType(StrEnum):
    YYYY_MM_DD = "%x"
    YYYY_MM_DD_HH24_MI_SS_US = "%x %H.%f"
    YYYY_MM_DD_HH12_MI_SS_US = "%x %I.%f %p"
    YYYY_MM_DD_HH12_MI_SS_MS = "%x %I.%g %p"
    YYYY_MM_DD_HH24_MI_SS_MS = "%x %H.%g"
    YYYY_MM_DD_HH24_MI_SSTZH_TZM = "%x %H.%g %z"
    YYYY_MM_DD_HH12_MI_SSTZH_TZM = "%x %I.%g %p %z"


class Evaluations(BaseModel):
    class ModelOutputType(StrEnum):
        PREDICTED_CLASS = "predicted_class"
        SCORE = "score"

    model_names: list
    metric: str
    filter_expression: str = ""
    window_size: PositiveInt = 1000
    limit: PositiveInt = 100
    is_web: bool = False
    output_type: Optional[ModelOutputType] = ModelOutputType.SCORE

    class Config:
        protected_namespaces = ()


class ModelScores(BaseModel):
    scores: List[float]
    timestamps: List[int]
    page: int
    next_page: Optional[List[int]] = None

    @validator("timestamps", pre=True, each_item=True)
    def convert_timestamp_to_epoch_microseconds(
        cls, value: Union[Timestamp, Any]
    ) -> int:
        if isinstance(value, Timestamp):
            return int(value.timestamp() * 1_000_000)
        return int(float(value) * 1_000_000)


class KafkaTopicInfo(BaseModel):
    name: str
    partitions: int
    replication_factor: int
    num_messages: int


class KafkaTopicSettings(BaseModel):
    # TODO(maniktherana): prune as much Optional as we can to get stronger types
    compression_type: Optional[str] = None
    leader_replication_throttled_replicas: Optional[str] = None
    remote_storage_enable: Optional[bool] = None
    message_downconversion_enable: Optional[bool] = None
    min_insync_replicas: Optional[int] = None
    segment_jitter_ms: Optional[int] = None
    local_retention_ms: Optional[int] = None
    cleanup_policy: Optional[str] = None
    flush_ms: Optional[int] = None
    follower_replication_throttled_replicas: Optional[str] = None
    segment_bytes: Optional[int] = None
    retention_ms: Optional[int] = None
    flush_messages: Optional[int] = None
    message_format_version: Optional[str] = None
    max_compaction_lag_ms: Optional[int] = None
    file_delete_delay_ms: Optional[int] = None
    max_message_bytes: Optional[int] = None
    min_compaction_lag_ms: Optional[int] = None
    message_timestamp_type: Optional[str] = None
    local_retention_bytes: Optional[int] = None
    preallocate: Optional[bool] = None
    index_interval_bytes: Optional[int] = None
    min_cleanable_dirty_ratio: Optional[float] = None
    unclean_leader_election_enable: Optional[bool] = None
    retention_bytes: Optional[int] = None
    delete_retention_ms: Optional[int] = None
    message_timestamp_after_max_ms: Optional[int] = None
    message_timestamp_before_max_ms: Optional[int] = None
    segment_ms: Optional[int] = None
    message_timestamp_difference_max_ms: Optional[int] = None
    segment_index_bytes: Optional[int] = None


class DetailedKafkaTopicInfo(BaseModel):
    name: str
    partitions: int
    replication_factor: int
    urp: int
    in_sync_replicas: int
    total_replicas: int
    cleanup_policy: str
    segment_size: int
    segment_count: int


class KafkaTopicConsumer(BaseModel):
    group_id: str
    active_consumers: int
    state: str


class SchemaInfo(BaseModel):
    subject: str
    id: int
    type: str
    version: int


class DetailedSchemaInfo(BaseModel):
    subject: str
    latest_version: int
    latest_id: int
    latest_type: str
    all_versions: list[SchemaInfo]


class ServiceEndpoints(BaseModel):
    arrow_server: str
    feature_server: str
