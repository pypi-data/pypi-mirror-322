# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.0.2](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.1 
# Pydantic Version: 2.10.4 
import typing
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from protobuf_to_pydantic.customer_validator import check_one_of
from pydantic import BaseModel, Field, model_validator


class DataDeliveryMode(IntEnum):
    STATIC = 0
    DYNAMIC = 1

class KafkaSource(BaseModel):
    topic: str = Field(default="")
    proto_message_name: str = Field(default="")
    schema_version: int = Field(default=0)

class FeatureGroupSource(BaseModel):
    name: str = Field(default="")

class S3Config(BaseModel):
    bucket: str = Field()
    access_key_id: typing.Optional[str] = Field(default="")
    secret_access_key: typing.Optional[str] = Field(default="")
    region: str = Field()
    endpoint: typing.Optional[str] = Field(default="")

class FileSource(BaseModel):
    class Format(IntEnum):
        CSV = 0
        JSON = 1
        AVRO = 2
        PARQUET = 3
        ORC = 4

    _one_of_dict = {"FileSource.storage_config": {"fields": {"s3_config"}, "required": True}}
    one_of_validator = model_validator(mode="before")(check_one_of)
    path: str = Field(default="")
    format: "FileSource.Format" = Field(default=0)
    s3_config: typing.Optional[S3Config] = Field(default=None)

class PostgresSource(BaseModel):
    host: str = Field(default="")
    port: int = Field(default=0)
    username: str = Field(default="")
    password: str = Field(default="")
    table: str = Field(default="")
    database: str = Field(default="")
    incrementing_column: str = Field(default="")
    timestamp_column: str = Field(default="")

class TimestampFormatConfig(BaseModel):
    class FormatType(IntEnum):
        EpochMillis = 0
        EpochSeconds = 1
        StringTimestamp = 2

    format_type: "TimestampFormatConfig.FormatType" = Field(default=0)
    format_string: typing.Optional[str] = Field(default="")
    time_zone: typing.Optional[str] = Field(default="")

class Watermark(BaseModel):
    time_col: str = Field(default="")
    allowed_delay_seconds: int = Field(default=0)
    time_col_config: typing.Optional[TimestampFormatConfig] = Field(default=None)

class DataSource(BaseModel):
    _one_of_dict = {"DataSource.type": {"fields": {"feature_group_source", "file_source", "kafka_source", "postgres_source"}, "required": True}}
    one_of_validator = model_validator(mode="before")(check_one_of)
    name: str = Field(default="", min_length=1, pattern="^[a-z]([a-z0-9_]{0,48}[a-z0-9])?$")
    key_fields: typing.List[str] = Field(default_factory=list)
    environment: typing.Optional[str] = Field(default="")
    encoded_schema: typing.Optional[str] = Field(default="")
    delivery_mode: DataDeliveryMode = Field(default=0)
    watermark: typing.Optional[Watermark] = Field(default=None)
    file_source: typing.Optional[FileSource] = Field(default=None)
    postgres_source: typing.Optional[PostgresSource] = Field(default=None)
    kafka_source: typing.Optional[KafkaSource] = Field(default=None)
    feature_group_source: typing.Optional[FeatureGroupSource] = Field(default=None)
