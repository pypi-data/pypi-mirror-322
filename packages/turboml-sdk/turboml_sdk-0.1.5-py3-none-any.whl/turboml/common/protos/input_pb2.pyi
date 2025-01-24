from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Input(_message.Message):
    __slots__ = ("numeric", "categ", "text", "images", "time_tick", "label", "key")
    NUMERIC_FIELD_NUMBER: _ClassVar[int]
    CATEG_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    TIME_TICK_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    numeric: _containers.RepeatedScalarFieldContainer[float]
    categ: _containers.RepeatedScalarFieldContainer[int]
    text: _containers.RepeatedScalarFieldContainer[str]
    images: _containers.RepeatedScalarFieldContainer[bytes]
    time_tick: int
    label: float
    key: str
    def __init__(self, numeric: _Optional[_Iterable[float]] = ..., categ: _Optional[_Iterable[int]] = ..., text: _Optional[_Iterable[str]] = ..., images: _Optional[_Iterable[bytes]] = ..., time_tick: _Optional[int] = ..., label: _Optional[float] = ..., key: _Optional[str] = ...) -> None: ...
