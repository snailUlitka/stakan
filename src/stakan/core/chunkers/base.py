"""Base class for chunkers."""

from typing import Protocol


class Chunker(Protocol):  # noqa: D101
    def split(self, document: str) -> list[str]:  # noqa: D102
        ...
