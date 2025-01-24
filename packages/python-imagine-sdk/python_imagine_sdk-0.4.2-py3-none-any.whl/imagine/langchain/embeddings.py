from __future__ import annotations

from pydantic import BaseModel

from imagine.langchain.mixins import BaseLangChainMixin


try:
    from langchain_core.embeddings import Embeddings
except ImportError:
    raise ImportError(
        "LangChain dependencies are missing. Please install with 'pip install python-imagine-sdk[langchain]' to add them."
    )


class ImagineEmbeddings(BaseModel, Embeddings, BaseLangChainMixin):
    """Imagine embedding models."""

    max_concurrent_requests: int = 64
    model: str = "BAAI/bge-large-en-v1.5"

    # TODO: Leverage asyncio to make it faster...
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of document texts.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        try:
            response = self.client.embeddings(texts=texts, model=self.model)

            return [embedding_obj.embedding for embedding_obj in response.data]
        except Exception:
            raise

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of document texts.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        try:
            response = await self.async_client.embeddings(text=texts, model=self.model)

            return [embedding_obj.embedding for embedding_obj in response.data]
        except Exception:
            raise

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query text.

        Args:
            text: The text to embed.

        Returns:
            Embedding for the text.
        """
        return self.embed_documents([text])[0]

    async def aembed_query(self, text: str) -> list[float]:
        """Embed a single query text.

        Args:
            text: The text to embed.

        Returns:
            Embedding for the text.
        """
        return (await self.aembed_documents([text]))[0]
