from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TarotSpreadRequest(_message.Message):
    __slots__ = ["question", "category", "spread_profile_id", "language"]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    SPREAD_PROFILE_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    question: str
    category: str
    spread_profile_id: str
    language: str
    def __init__(self, question: _Optional[str] = ..., category: _Optional[str] = ..., spread_profile_id: _Optional[str] = ..., language: _Optional[str] = ...) -> None: ...

class TarotSpreadResponse(_message.Message):
    __slots__ = ["question", "category", "spread"]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    SPREAD_FIELD_NUMBER: _ClassVar[int]
    question: str
    category: str
    spread: str
    def __init__(self, question: _Optional[str] = ..., category: _Optional[str] = ..., spread: _Optional[str] = ...) -> None: ...

class TarotSpreadConfigRequest(_message.Message):
    __slots__ = ["spread_profile_id", "category", "question", "language"]
    SPREAD_PROFILE_ID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    spread_profile_id: str
    category: str
    question: str
    language: str
    def __init__(self, spread_profile_id: _Optional[str] = ..., category: _Optional[str] = ..., question: _Optional[str] = ..., language: _Optional[str] = ...) -> None: ...

class TarotSpreadConfigResponse(_message.Message):
    __slots__ = ["id", "spread_prompt"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SPREAD_PROMPT_FIELD_NUMBER: _ClassVar[int]
    id: str
    spread_prompt: str
    def __init__(self, id: _Optional[str] = ..., spread_prompt: _Optional[str] = ...) -> None: ...

class SaveSpreadRequest(_message.Message):
    __slots__ = ["spread_profile_id", "spread", "question", "category", "language"]
    SPREAD_PROFILE_ID_FIELD_NUMBER: _ClassVar[int]
    SPREAD_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    spread_profile_id: str
    spread: str
    question: str
    category: str
    language: str
    def __init__(self, spread_profile_id: _Optional[str] = ..., spread: _Optional[str] = ..., question: _Optional[str] = ..., category: _Optional[str] = ..., language: _Optional[str] = ...) -> None: ...
