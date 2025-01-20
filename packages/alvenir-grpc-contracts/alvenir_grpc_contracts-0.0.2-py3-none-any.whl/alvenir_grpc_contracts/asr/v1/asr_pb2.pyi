from alvenir_grpc_contracts.types.v1 import format_pb2 as _format_pb2
from alvenir_grpc_contracts.types.v1 import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BidiStreamAudioRequest(_message.Message):
    __slots__ = ("metadata", "audio_data")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    AUDIO_DATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _format_pb2.AudioMetaData
    audio_data: _format_pb2.AudioChunk
    def __init__(self, metadata: _Optional[_Union[_format_pb2.AudioMetaData, _Mapping]] = ..., audio_data: _Optional[_Union[_format_pb2.AudioChunk, _Mapping]] = ...) -> None: ...

class StreamAudioRequest(_message.Message):
    __slots__ = ("metadata", "audio_data")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    AUDIO_DATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _format_pb2.AudioMetaData
    audio_data: _format_pb2.AudioChunk
    def __init__(self, metadata: _Optional[_Union[_format_pb2.AudioMetaData, _Mapping]] = ..., audio_data: _Optional[_Union[_format_pb2.AudioChunk, _Mapping]] = ...) -> None: ...

class StreamAudioResponse(_message.Message):
    __slots__ = ("call_id", "status")
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    call_id: str
    status: _status_pb2.ResponseStatus
    def __init__(self, call_id: _Optional[str] = ..., status: _Optional[_Union[_status_pb2.ResponseStatus, str]] = ...) -> None: ...

class GetTranscriptionRequest(_message.Message):
    __slots__ = ("call_id",)
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    call_id: str
    def __init__(self, call_id: _Optional[str] = ...) -> None: ...

class GetTranscriptionResponse(_message.Message):
    __slots__ = ("transcript",)
    TRANSCRIPT_FIELD_NUMBER: _ClassVar[int]
    transcript: str
    def __init__(self, transcript: _Optional[str] = ...) -> None: ...

class BidiStreamAudioResponse(_message.Message):
    __slots__ = ("partial_transcript",)
    PARTIAL_TRANSCRIPT_FIELD_NUMBER: _ClassVar[int]
    partial_transcript: str
    def __init__(self, partial_transcript: _Optional[str] = ...) -> None: ...
