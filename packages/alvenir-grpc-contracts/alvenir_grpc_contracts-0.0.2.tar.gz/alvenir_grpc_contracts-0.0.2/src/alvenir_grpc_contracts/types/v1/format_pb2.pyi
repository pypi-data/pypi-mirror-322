from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PCM(_message.Message):
    __slots__ = ("sample_rate", "channels", "sample_width")
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    sample_rate: int
    channels: int
    sample_width: int
    def __init__(self, sample_rate: _Optional[int] = ..., channels: _Optional[int] = ..., sample_width: _Optional[int] = ...) -> None: ...

class AudioMetaData(_message.Message):
    __slots__ = ("advisor_id", "caller_id", "chunk_size", "pcm_format", "processing_id")
    ADVISOR_ID_FIELD_NUMBER: _ClassVar[int]
    CALLER_ID_FIELD_NUMBER: _ClassVar[int]
    CHUNK_SIZE_FIELD_NUMBER: _ClassVar[int]
    PCM_FORMAT_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_ID_FIELD_NUMBER: _ClassVar[int]
    advisor_id: str
    caller_id: str
    chunk_size: int
    pcm_format: PCM
    processing_id: str
    def __init__(self, advisor_id: _Optional[str] = ..., caller_id: _Optional[str] = ..., chunk_size: _Optional[int] = ..., pcm_format: _Optional[_Union[PCM, _Mapping]] = ..., processing_id: _Optional[str] = ...) -> None: ...

class AudioChunk(_message.Message):
    __slots__ = ("audio_advisor", "audio_caller")
    AUDIO_ADVISOR_FIELD_NUMBER: _ClassVar[int]
    AUDIO_CALLER_FIELD_NUMBER: _ClassVar[int]
    audio_advisor: bytes
    audio_caller: bytes
    def __init__(self, audio_advisor: _Optional[bytes] = ..., audio_caller: _Optional[bytes] = ...) -> None: ...
