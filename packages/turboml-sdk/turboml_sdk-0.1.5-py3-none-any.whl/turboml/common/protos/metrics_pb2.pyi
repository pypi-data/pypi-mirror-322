from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Metrics(_message.Message):
    __slots__ = ("index", "metric")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    index: int
    metric: float
    def __init__(self, index: _Optional[int] = ..., metric: _Optional[float] = ...) -> None: ...
