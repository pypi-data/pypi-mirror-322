from alvenir_grpc_contracts.types.v1 import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PostSummaryAnalyticsRequest(_message.Message):
    __slots__ = ("call_id", "edited_summary", "wrap_up_time_seconds")
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    EDITED_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    WRAP_UP_TIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    call_id: str
    edited_summary: str
    wrap_up_time_seconds: float
    def __init__(self, call_id: _Optional[str] = ..., edited_summary: _Optional[str] = ..., wrap_up_time_seconds: _Optional[float] = ...) -> None: ...

class PostSummaryAnalyticsResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: _status_pb2.ResponseStatus
    message: str
    def __init__(self, status: _Optional[_Union[_status_pb2.ResponseStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...
