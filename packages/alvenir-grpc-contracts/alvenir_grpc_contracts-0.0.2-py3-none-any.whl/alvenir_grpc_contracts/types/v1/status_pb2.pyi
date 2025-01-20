from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ResponseStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESPONSE_STATUS_UNSPECIFIED: _ClassVar[ResponseStatus]
    RESPONSE_STATUS_OK: _ClassVar[ResponseStatus]
    RESPONSE_STATUS_ERROR: _ClassVar[ResponseStatus]
RESPONSE_STATUS_UNSPECIFIED: ResponseStatus
RESPONSE_STATUS_OK: ResponseStatus
RESPONSE_STATUS_ERROR: ResponseStatus
