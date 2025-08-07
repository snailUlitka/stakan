"""Tests for OpenAI (and API compability) embedding models."""

import time
from types import SimpleNamespace

import pytest
import requests

from stakan.core.embedding_models.openai import OpenAIEmbedding
from tests.config import Settings

# TODO: Add integration tests with Ollama, etc.
# https://github.com/snailUlitka/stakan/issues/21


@pytest.mark.integration
def test_ollama_connection(settings: Settings):
    if not settings.use_ollama:
        pytest.skip("Ollama usage disabled in tests")
    for _ in range(10):
        try:
            resp = requests.get(f"{settings.ollama_url}/models", timeout=5)
            if resp.status_code == 200:
                break
        except requests.ConnectionError:
            time.sleep(1)
    else:
        pytest.skip("Ollama-server don't response, try to start Ollama-server")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    data = resp.json()
    assert "data" in data
    assert isinstance(data["data"], list)


@pytest.mark.integration
def test_embedding_method(settings: Settings):
    if not settings.use_ollama:
        pytest.skip("Ollama usage disabled in tests")
    emb = OpenAIEmbedding(
        model=settings.model_name,
        api_key=settings.api_key,
        base_url=str(settings.ollama_url),
    )

    result = emb.embedding("test query")

    assert isinstance(result, tuple)
    assert all(isinstance(x, float) for x in result)


@pytest.mark.unit
def test_embedding_method_monkeypatch(monkeypatch: pytest.MonkeyPatch):
    dummy_embedding = [0.1, 0.2, 0.3]

    class DummyClient:
        def __init__(self, *_args, **_kwargs) -> None:  # noqa: ANN002, ANN003
            self.embeddings = SimpleNamespace(
                create=lambda input, model: SimpleNamespace(  # noqa: A006, ARG005
                    data=[SimpleNamespace(embedding=dummy_embedding)]
                )
            )

    monkeypatch.setattr(
        "stakan.core.embedding_models.openai.OpenAI",
        DummyClient,
    )

    emb = OpenAIEmbedding(model="dummy-model", api_key="key", base_url="url")
    result = emb.embedding("test query")
    assert isinstance(result, tuple)
    assert result == tuple(dummy_embedding)
    assert all(isinstance(x, float) for x in result)
