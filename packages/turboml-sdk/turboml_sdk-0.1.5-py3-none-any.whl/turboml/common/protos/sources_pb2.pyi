from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataDeliveryMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATIC: _ClassVar[DataDeliveryMode]
    DYNAMIC: _ClassVar[DataDeliveryMode]
STATIC: DataDeliveryMode
DYNAMIC: DataDeliveryMode

class KafkaSource(_message.Message):
    __slots__ = ("topic", "proto_message_name", "schema_version")
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    PROTO_MESSAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    topic: str
    proto_message_name: str
    schema_version: int
    def __init__(self, topic: _Optional[str] = ..., proto_message_name: _Optional[str] = ..., schema_version: _Optional[int] = ...) -> None: ...

class FeatureGroupSource(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class S3Config(_message.Message):
    __slots__ = ("bucket", "access_key_id", "secret_access_key", "region", "endpoint")
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    access_key_id: str
    secret_access_key: str
    region: str
    endpoint: str
    def __init__(self, bucket: _Optional[str] = ..., access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ..., region: _Optional[str] = ..., endpoint: _Optional[str] = ...) -> None: ...

class FileSource(_message.Message):
    __slots__ = ("path", "format", "s3_config")
    class Format(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CSV: _ClassVar[FileSource.Format]
        JSON: _ClassVar[FileSource.Format]
        AVRO: _ClassVar[FileSource.Format]
        PARQUET: _ClassVar[FileSource.Format]
        ORC: _ClassVar[FileSource.Format]
    CSV: FileSource.Format
    JSON: FileSource.Format
    AVRO: FileSource.Format
    PARQUET: FileSource.Format
    ORC: FileSource.Format
    PATH_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    S3_CONFIG_FIELD_NUMBER: _ClassVar[int]
    path: str
    format: FileSource.Format
    s3_config: S3Config
    def __init__(self, path: _Optional[str] = ..., format: _Optional[_Union[FileSource.Format, str]] = ..., s3_config: _Optional[_Union[S3Config, _Mapping]] = ...) -> None: ...

class PostgresSource(_message.Message):
    __slots__ = ("host", "port", "username", "password", "table", "database", "incrementing_column", "timestamp_column")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    INCREMENTING_COLUMN_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_COLUMN_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    username: str
    password: str
    table: str
    database: str
    incrementing_column: str
    timestamp_column: str
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., table: _Optional[str] = ..., database: _Optional[str] = ..., incrementing_column: _Optional[str] = ..., timestamp_column: _Optional[str] = ...) -> None: ...

class TimestampFormatConfig(_message.Message):
    __slots__ = ("format_type", "format_string", "time_zone")
    class FormatType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        EpochMillis: _ClassVar[TimestampFormatConfig.FormatType]
        EpochSeconds: _ClassVar[TimestampFormatConfig.FormatType]
        StringTimestamp: _ClassVar[TimestampFormatConfig.FormatType]
    EpochMillis: TimestampFormatConfig.FormatType
    EpochSeconds: TimestampFormatConfig.FormatType
    StringTimestamp: TimestampFormatConfig.FormatType
    FORMAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_STRING_FIELD_NUMBER: _ClassVar[int]
    TIME_ZONE_FIELD_NUMBER: _ClassVar[int]
    format_type: TimestampFormatConfig.FormatType
    format_string: str
    time_zone: str
    def __init__(self, format_type: _Optional[_Union[TimestampFormatConfig.FormatType, str]] = ..., format_string: _Optional[str] = ..., time_zone: _Optional[str] = ...) -> None: ...

class Watermark(_message.Message):
    __slots__ = ("time_col", "allowed_delay_seconds", "time_col_config")
    TIME_COL_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_DELAY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TIME_COL_CONFIG_FIELD_NUMBER: _ClassVar[int]
    time_col: str
    allowed_delay_seconds: int
    time_col_config: TimestampFormatConfig
    def __init__(self, time_col: _Optional[str] = ..., allowed_delay_seconds: _Optional[int] = ..., time_col_config: _Optional[_Union[TimestampFormatConfig, _Mapping]] = ...) -> None: ...

class DataSource(_message.Message):
    __slots__ = ("name", "key_fields", "environment", "encoded_schema", "delivery_mode", "watermark", "file_source", "postgres_source", "kafka_source", "feature_group_source")
    NAME_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELDS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    ENCODED_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_MODE_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_FIELD_NUMBER: _ClassVar[int]
    FILE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    POSTGRES_SOURCE_FIELD_NUMBER: _ClassVar[int]
    KAFKA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_GROUP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    name: str
    key_fields: _containers.RepeatedScalarFieldContainer[str]
    environment: str
    encoded_schema: str
    delivery_mode: DataDeliveryMode
    watermark: Watermark
    file_source: FileSource
    postgres_source: PostgresSource
    kafka_source: KafkaSource
    feature_group_source: FeatureGroupSource
    def __init__(self, name: _Optional[str] = ..., key_fields: _Optional[_Iterable[str]] = ..., environment: _Optional[str] = ..., encoded_schema: _Optional[str] = ..., delivery_mode: _Optional[_Union[DataDeliveryMode, str]] = ..., watermark: _Optional[_Union[Watermark, _Mapping]] = ..., file_source: _Optional[_Union[FileSource, _Mapping]] = ..., postgres_source: _Optional[_Union[PostgresSource, _Mapping]] = ..., kafka_source: _Optional[_Union[KafkaSource, _Mapping]] = ..., feature_group_source: _Optional[_Union[FeatureGroupSource, _Mapping]] = ...) -> None: ...
