from __future__ import annotations

from pydantic import BaseModel

from imagine.types.common import UsageInfo


class EmbeddingObject(BaseModel):
    #: The object type, which is always "embedding"
    object: str

    #: The index of the embedding in the list of embeddings.
    embedding: list[float]

    #: The embedding vector, which is a list of floats. The length of vector depends on the model
    index: int


class EmbeddingResponse(BaseModel):
    #: Unique object identifier.
    id: str

    #: The object type, which is always "list".
    object: str

    data: list[EmbeddingObject]

    #: Model name used.
    model: str

    ##: Usage statistics.
    usage: UsageInfo

    @property
    def first_embedding(self) -> list[float]:
        """
        Gets the first content from the response

        :return: embedding content
        """
        return self.data[0].embedding


class EmbeddingRequest(BaseModel):
    #: Unique object identifier.
    id: str | None

    #: Input string for which embedding should be generated
    input: str

    #: Model to be used for generation of embedding
    model: str
