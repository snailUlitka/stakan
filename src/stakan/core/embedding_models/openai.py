"""Class for any embedding models with OpenAI API compatibility."""

from openai import OpenAI

# TODO: Add support for async client version (AsyncOpenAI)
# https://github.com/snailUlitka/stakan/issues/13


class OpenAIEmbedding:
    """Embedding model with OpenAI API compatibility."""

    def __init__(
        self,
        model: str,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self._model = model
        self._client = OpenAI(api_key=api_key, base_url=base_url)

    # TODO: Add support for generate embeddings in batch request
    # https://github.com/snailUlitka/stakan/issues/14

    def embedding(self, query: str) -> tuple[float, ...]:
        """Generate embedding for given query.

        Returns
        -------
        tuple[float, ...]
            Tuple with floats, dimensions based on provided embedding model.
        """
        result = self._client.embeddings.create(
            input=query,
            model=self._model,
        )

        return tuple(result.data[0].embedding)
