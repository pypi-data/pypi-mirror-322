from enum import Enum


class ModelType(str, Enum):
    """
    Supported values: `ModelType.EMBEDDING`,`ModelType.LLM`, `ModelType.RERANKER`, `ModelType.TEXT_TO_IMAGE`, `ModelType.TRANSCRIBE`, `ModelType.TRANSLATE`.
    """

    EMBEDDING = "embedding"
    LLM = "llm"
    RERANKER = "reranker"
    TEXT_TO_IMAGE = "text_to_image"
    TRANSCRIBE = "transcribe"
    TRANSLATE = "translate"

    def __repr__(self) -> str:
        return "<%s.%s>" % (self.__class__.__name__, self._name_)
