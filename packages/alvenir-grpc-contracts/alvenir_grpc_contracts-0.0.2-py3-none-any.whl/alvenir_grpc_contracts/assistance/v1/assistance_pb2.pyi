from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Importance(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IMPORTANCE_UNSPECIFIED: _ClassVar[Importance]
    IMPORTANCE_LOW: _ClassVar[Importance]
    IMPORTANCE_HIGH: _ClassVar[Importance]
IMPORTANCE_UNSPECIFIED: Importance
IMPORTANCE_LOW: Importance
IMPORTANCE_HIGH: Importance

class Action(_message.Message):
    __slots__ = ("text", "url")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    text: str
    url: str
    def __init__(self, text: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class AssistanceEvent(_message.Message):
    __slots__ = ("title", "body", "action", "importance", "key", "processing_id")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    IMPORTANCE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_ID_FIELD_NUMBER: _ClassVar[int]
    title: str
    body: str
    action: Action
    importance: Importance
    key: str
    processing_id: str
    def __init__(self, title: _Optional[str] = ..., body: _Optional[str] = ..., action: _Optional[_Union[Action, _Mapping]] = ..., importance: _Optional[_Union[Importance, str]] = ..., key: _Optional[str] = ..., processing_id: _Optional[str] = ...) -> None: ...
