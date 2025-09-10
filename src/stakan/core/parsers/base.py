"""Base class for parsers."""

from typing import Protocol


class Parser(Protocol):  # noqa: D101
    def parse(self, document: bytes) -> str:  # noqa: D102
        ...
