from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PingRequest(_message.Message):
    __slots__ = ("wait_time",)
    WAIT_TIME_FIELD_NUMBER: _ClassVar[int]
    wait_time: int
    def __init__(self, wait_time: _Optional[int] = ...) -> None: ...

class PingResponse(_message.Message):
    __slots__ = ("request_received_utc", "response_sent_utc")
    REQUEST_RECEIVED_UTC_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_SENT_UTC_FIELD_NUMBER: _ClassVar[int]
    request_received_utc: int
    response_sent_utc: int
    def __init__(self, request_received_utc: _Optional[int] = ..., response_sent_utc: _Optional[int] = ...) -> None: ...
