from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Output(_message.Message):
    __slots__ = ("key", "score", "feature_score", "class_probabilities", "predicted_class", "embeddings", "text_output")
    KEY_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SCORE_FIELD_NUMBER: _ClassVar[int]
    CLASS_PROBABILITIES_FIELD_NUMBER: _ClassVar[int]
    PREDICTED_CLASS_FIELD_NUMBER: _ClassVar[int]
    EMBEDDINGS_FIELD_NUMBER: _ClassVar[int]
    TEXT_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    key: str
    score: float
    feature_score: _containers.RepeatedScalarFieldContainer[float]
    class_probabilities: _containers.RepeatedScalarFieldContainer[float]
    predicted_class: int
    embeddings: _containers.RepeatedScalarFieldContainer[float]
    text_output: str
    def __init__(self, key: _Optional[str] = ..., score: _Optional[float] = ..., feature_score: _Optional[_Iterable[float]] = ..., class_probabilities: _Optional[_Iterable[float]] = ..., predicted_class: _Optional[int] = ..., embeddings: _Optional[_Iterable[float]] = ..., text_output: _Optional[str] = ...) -> None: ...
