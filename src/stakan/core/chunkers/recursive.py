"""Module with recursive chunker for text splitting into fixed-size chunks."""


class Recursive:
    r"""
    A class for recursively splitting string documents into chunks.

    Parameters
    ----------
        chunk_size (int): Maximum length of each chunk.
        overlap (int): Number of characters to overlap between consecutive chunks.
        split_by (tuple[str, ...]): Sequence of separators to use for
            hierarchical splitting. The higher priority separators come first.
            (e.g. "\n\n" > "\t")
    """

    def __init__(
        self,
        chunk_size: int = 8000,
        overlap: int = 200,
        split_by: tuple[str, ...] = ("\n\n", "\n", "\t", " "),
    ) -> None:
        self._chunk_size = chunk_size
        self._overlap = overlap
        self._split_by = split_by

    def split(self, document: str) -> list[str]:
        """
        Recursively split the `document` into chunks.

        Chunks can't be longer than `chunk_size`. Each chunk can overlap
        the previous one and the next one by `overlap` characters.

        Algorithm:
        1. If the text length is <= chunk_size, return it as a single chunk.
        2. Otherwise, try splitting the text on the first separator in split_by.
           a) If all resulting parts are <= chunk_size, merge them into chunks
              respecting chunk_size and adding overlap between chunks.
           b) If any part still exceeds chunk_size, recursively split that part
              using the remaining separators.
        3. If no separators remain, perform hard splits into fixed-size segments
           with the given overlap.

        Parameters
        ----------
            document (str): The full text to be split.

        Returns
        -------
            A list of text chunks.
        """
        return self._recursive_split(document, self._split_by)

    def _recursive_split(self, text: str, separators: tuple[str, ...]) -> list[str]:
        """Recursively split text using the provided separators."""
        if len(text) <= self._chunk_size:
            return [text]

        if not separators:
            return self._hard_split(text)

        sep, *rest = separators
        parts = [p for p in text.split(sep) if p]

        if all(len(part) <= self._chunk_size for part in parts):
            return self._merge_parts(parts, sep)

        chunks = []
        for part in parts:
            chunks.extend(self._recursive_split(part, tuple(rest)))

        return chunks

    def _hard_split(self, text: str) -> list[str]:
        """Perform fixed-size splits with overlap when no separators remain."""
        step = self._chunk_size

        if self._overlap < self._chunk_size:
            step -= self._overlap

        if step <= 0:
            msg = (
                f"Invalid split step: {step} (chunk_size={self._chunk_size}, "
                f"overlap={self._overlap})"
            )
            raise ValueError(msg)

        return [text[i : i + self._chunk_size] for i in range(0, len(text), step)]

    def _merge_parts(self, parts: list[str], sep: str) -> list[str]:
        """Merge small parts into chunks up to `chunk_size`, then apply overlap."""
        merged = []
        current = ""

        for part in parts:
            addition = (sep + part) if current else part

            if len(current) + len(addition) <= self._chunk_size:
                current += addition
            else:
                merged.append(current)
                current = part

        if current:
            merged.append(current)

        if self._overlap <= 0:
            return merged

        overlapped = []

        for idx, chunk in enumerate(merged):
            if idx == 0:
                overlapped.append(chunk)
            else:
                prefix = merged[idx - 1][-self._overlap :]
                overlapped.append(prefix + chunk)

        return overlapped
