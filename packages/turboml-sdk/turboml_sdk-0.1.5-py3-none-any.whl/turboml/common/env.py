from __future__ import annotations
from pydantic import Field  # noqa: TCH002
from pydantic_settings import BaseSettings, SettingsConfigDict


class _TurboMLConfig(BaseSettings):
    model_config = SettingsConfigDict(frozen=True)

    TURBOML_BACKEND_SERVER_ADDRESS: str = Field(default="http://localhost:8500")
    FEATURE_SERVER_ADDRESS: str = Field(default="grpc+tcp://localhost:8552")
    ARROW_SERVER_ADDRESS: str = Field(default="grpc+tcp://localhost:8502")

    def set_backend_server(self, value: str):
        object.__setattr__(self, "TURBOML_BACKEND_SERVER_ADDRESS", value)

    def set_feature_server(self, value: str):
        object.__setattr__(self, "FEATURE_SERVER_ADDRESS", value)

    def set_arrow_server(self, value: str):
        object.__setattr__(self, "ARROW_SERVER_ADDRESS", value)


# Global config object
CONFIG = _TurboMLConfig()  # type: ignore
