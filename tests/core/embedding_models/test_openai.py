"""Tests for OpenAI (and API compability) embedding models."""

import os
import time
from types import SimpleNamespace

import pytest
import requests

from stakan.core.embedding_models.openai import OpenAIEmbedding

# TODO: Add global test configuration with Pydantic-Settings
# https://github.com/snailUlitka/stakan/issues/17


@pytest.fixture(scope="session")
def ollama_url() -> str:
    return os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")


@pytest.fixture(scope="session")
def model_name() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", "nomic-embed-text")


def test_ollama_connection(ollama_url: str):
    for _ in range(10):
        try:
            resp = requests.get(f"{ollama_url}/models", timeout=5)
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


def test_embedding_method(ollama_url: str, model_name: str):
    emb = OpenAIEmbedding(model=model_name, api_key="ollama", base_url=ollama_url)

    result = emb.embedding("test query")

    assert isinstance(result, tuple)
    assert all(isinstance(x, float) for x in result)


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
