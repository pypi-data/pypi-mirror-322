from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LlmPromptAnswer(_message.Message):
    __slots__ = ("prompt", "meta", "answer", "score")
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    meta: str
    answer: str
    score: float
    def __init__(self, prompt: _Optional[str] = ..., meta: _Optional[str] = ..., answer: _Optional[str] = ..., score: _Optional[float] = ...) -> None: ...

class LlmData(_message.Message):
    __slots__ = ("introduction", "client_satisfaction", "answer_quality", "empathy", "language", "voice", "speaker_efficiency", "upselling", "general_feedback", "subjects")
    INTRODUCTION_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SATISFACTION_FIELD_NUMBER: _ClassVar[int]
    ANSWER_QUALITY_FIELD_NUMBER: _ClassVar[int]
    EMPATHY_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    VOICE_FIELD_NUMBER: _ClassVar[int]
    SPEAKER_EFFICIENCY_FIELD_NUMBER: _ClassVar[int]
    UPSELLING_FIELD_NUMBER: _ClassVar[int]
    GENERAL_FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    SUBJECTS_FIELD_NUMBER: _ClassVar[int]
    introduction: LlmPromptAnswer
    client_satisfaction: LlmPromptAnswer
    answer_quality: LlmPromptAnswer
    empathy: LlmPromptAnswer
    language: LlmPromptAnswer
    voice: LlmPromptAnswer
    speaker_efficiency: LlmPromptAnswer
    upselling: LlmPromptAnswer
    general_feedback: LlmPromptAnswer
    subjects: LlmPromptAnswer
    def __init__(self, introduction: _Optional[_Union[LlmPromptAnswer, _Mapping]] = ..., client_satisfaction: _Optional[_Union[LlmPromptAnswer, _Mapping]] = ..., answer_quality: _Optional[_Union[LlmPromptAnswer, _Mapping]] = ..., empathy: _Optional[_Union[LlmPromptAnswer, _Mapping]] = ..., language: _Optional[_Union[LlmPromptAnswer, _Mapping]] = ..., voice: _Optional[_Union[LlmPromptAnswer, _Mapping]] = ..., speaker_efficiency: _Optional[_Union[LlmPromptAnswer, _Mapping]] = ..., upselling: _Optional[_Union[LlmPromptAnswer, _Mapping]] = ..., general_feedback: _Optional[_Union[LlmPromptAnswer, _Mapping]] = ..., subjects: _Optional[_Union[LlmPromptAnswer, _Mapping]] = ...) -> None: ...

class CallMeta(_message.Message):
    __slots__ = ("time_of_call", "length", "answer_time")
    TIME_OF_CALL_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    ANSWER_TIME_FIELD_NUMBER: _ClassVar[int]
    time_of_call: str
    length: float
    answer_time: float
    def __init__(self, time_of_call: _Optional[str] = ..., length: _Optional[float] = ..., answer_time: _Optional[float] = ...) -> None: ...

class TranscriptionMeta(_message.Message):
    __slots__ = ("n_words", "n_fill_words")
    N_WORDS_FIELD_NUMBER: _ClassVar[int]
    N_FILL_WORDS_FIELD_NUMBER: _ClassVar[int]
    n_words: str
    n_fill_words: str
    def __init__(self, n_words: _Optional[str] = ..., n_fill_words: _Optional[str] = ...) -> None: ...

class TimeInterval(_message.Message):
    __slots__ = ("start", "end")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: str
    end: str
    def __init__(self, start: _Optional[str] = ..., end: _Optional[str] = ...) -> None: ...

class TimeLineData(_message.Message):
    __slots__ = ("speaker", "interval_data")
    SPEAKER_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_DATA_FIELD_NUMBER: _ClassVar[int]
    speaker: str
    interval_data: _containers.RepeatedCompositeFieldContainer[TimeInterval]
    def __init__(self, speaker: _Optional[str] = ..., interval_data: _Optional[_Iterable[_Union[TimeInterval, _Mapping]]] = ...) -> None: ...

class TimeLineConcat(_message.Message):
    __slots__ = ("caller_data", "advisor_data")
    CALLER_DATA_FIELD_NUMBER: _ClassVar[int]
    ADVISOR_DATA_FIELD_NUMBER: _ClassVar[int]
    caller_data: TimeLineData
    advisor_data: TimeLineData
    def __init__(self, caller_data: _Optional[_Union[TimeLineData, _Mapping]] = ..., advisor_data: _Optional[_Union[TimeLineData, _Mapping]] = ...) -> None: ...

class SentimentCoordinates(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class SentimentData(_message.Message):
    __slots__ = ("speaker", "data_points")
    SPEAKER_FIELD_NUMBER: _ClassVar[int]
    DATA_POINTS_FIELD_NUMBER: _ClassVar[int]
    speaker: str
    data_points: _containers.RepeatedCompositeFieldContainer[SentimentCoordinates]
    def __init__(self, speaker: _Optional[str] = ..., data_points: _Optional[_Iterable[_Union[SentimentCoordinates, _Mapping]]] = ...) -> None: ...

class SentimentConcat(_message.Message):
    __slots__ = ("caller_data", "advisor_data")
    CALLER_DATA_FIELD_NUMBER: _ClassVar[int]
    ADVISOR_DATA_FIELD_NUMBER: _ClassVar[int]
    caller_data: SentimentData
    advisor_data: SentimentData
    def __init__(self, caller_data: _Optional[_Union[SentimentData, _Mapping]] = ..., advisor_data: _Optional[_Union[SentimentData, _Mapping]] = ...) -> None: ...

class GuidanceEvent(_message.Message):
    __slots__ = ("llm_data", "audio_segments", "sentiment_data", "audio_meta", "transcription_meta", "processing_id")
    LLM_DATA_FIELD_NUMBER: _ClassVar[int]
    AUDIO_SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    SENTIMENT_DATA_FIELD_NUMBER: _ClassVar[int]
    AUDIO_META_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPTION_META_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_ID_FIELD_NUMBER: _ClassVar[int]
    llm_data: LlmData
    audio_segments: TimeLineConcat
    sentiment_data: SentimentConcat
    audio_meta: CallMeta
    transcription_meta: TranscriptionMeta
    processing_id: str
    def __init__(self, llm_data: _Optional[_Union[LlmData, _Mapping]] = ..., audio_segments: _Optional[_Union[TimeLineConcat, _Mapping]] = ..., sentiment_data: _Optional[_Union[SentimentConcat, _Mapping]] = ..., audio_meta: _Optional[_Union[CallMeta, _Mapping]] = ..., transcription_meta: _Optional[_Union[TranscriptionMeta, _Mapping]] = ..., processing_id: _Optional[str] = ...) -> None: ...
