from alvenir_grpc_contracts.types.v1 import format_pb2 as _format_pb2
from alvenir_grpc_contracts.types.v1 import status_pb2 as _status_pb2
from alvenir_grpc_contracts.types.v1 import ping_pb2 as _ping_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StreamAudioRequest(_message.Message):
    __slots__ = ("metadata", "audio_data")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    AUDIO_DATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _format_pb2.AudioMetaData
    audio_data: _format_pb2.AudioChunk
    def __init__(self, metadata: _Optional[_Union[_format_pb2.AudioMetaData, _Mapping]] = ..., audio_data: _Optional[_Union[_format_pb2.AudioChunk, _Mapping]] = ...) -> None: ...

class StreamAudioResponse(_message.Message):
    __slots__ = ("status", "message", "call_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    status: _status_pb2.ResponseStatus
    message: str
    call_id: str
    def __init__(self, status: _Optional[_Union[_status_pb2.ResponseStatus, str]] = ..., message: _Optional[str] = ..., call_id: _Optional[str] = ...) -> None: ...

class StreamAndGetSummaryRequest(_message.Message):
    __slots__ = ("metadata", "audio_data")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    AUDIO_DATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _format_pb2.AudioMetaData
    audio_data: _format_pb2.AudioChunk
    def __init__(self, metadata: _Optional[_Union[_format_pb2.AudioMetaData, _Mapping]] = ..., audio_data: _Optional[_Union[_format_pb2.AudioChunk, _Mapping]] = ...) -> None: ...

class StreamAndGetSummaryResponse(_message.Message):
    __slots__ = ("status", "message", "results", "call_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    status: _status_pb2.ResponseStatus
    message: str
    results: AggregatedResults
    call_id: str
    def __init__(self, status: _Optional[_Union[_status_pb2.ResponseStatus, str]] = ..., message: _Optional[str] = ..., results: _Optional[_Union[AggregatedResults, _Mapping]] = ..., call_id: _Optional[str] = ...) -> None: ...

class GetSummaryRequest(_message.Message):
    __slots__ = ("call_id",)
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    call_id: str
    def __init__(self, call_id: _Optional[str] = ...) -> None: ...

class GetSummaryResponse(_message.Message):
    __slots__ = ("status", "message", "results")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    status: _status_pb2.ResponseStatus
    message: str
    results: AggregatedResults
    def __init__(self, status: _Optional[_Union[_status_pb2.ResponseStatus, str]] = ..., message: _Optional[str] = ..., results: _Optional[_Union[AggregatedResults, _Mapping]] = ...) -> None: ...

class AggregatedResults(_message.Message):
    __slots__ = ("transcription", "main_points", "journal_note")
    TRANSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MAIN_POINTS_FIELD_NUMBER: _ClassVar[int]
    JOURNAL_NOTE_FIELD_NUMBER: _ClassVar[int]
    transcription: str
    main_points: str
    journal_note: str
    def __init__(self, transcription: _Optional[str] = ..., main_points: _Optional[str] = ..., journal_note: _Optional[str] = ...) -> None: ...
