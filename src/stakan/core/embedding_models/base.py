"""Base class for embedding models wrapper."""

from typing import Protocol


class Embedding(Protocol):  # noqa: D101
    def embedding(self, query: str) -> tuple[float, ...]:  # noqa: D102
        ...
