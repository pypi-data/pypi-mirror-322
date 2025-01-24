from __future__ import annotations

from pydantic import BaseModel

from imagine.types.common import UsageInfo


class ReRankerObject(BaseModel):
    #: The text of the document
    document: str | None = None

    #: The index of the document
    index: int

    #: The relevance score of the document
    relevance_score: float


class ReRankerResponse(BaseModel):
    #: A unique identifier for the response
    id: str

    #: A list of ReRankerObject objects
    data: list[ReRankerObject]

    #: An error message if the request failed
    failure: str | None = None

    #: The name of the model used to generate the response
    model: str

    #: The type of object being returned
    object: str

    #: Information about the usage of the model
    usage: UsageInfo


class ReRankerRequest(BaseModel):
    #: The query string to be used for re-ranking
    query: str

    #: A list of document IDs or text
    documents: list[str]

    #: The number of top results to return (default: 1)
    top_n: int | None = None

    #: The name of the model to use for re-ranking
    model: str

    #: Whether to return the documents themselves (default: False)
    return_documents: bool | None = None
