"""Test configuration utilities."""

import pytest
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration for tests."""

    model_name: str = "nomic-embed-text"
    use_ollama: bool = False
    ollama_url: HttpUrl = "http://localhost:11434/v1"
    api_key: str = "ollama"

    model_config = SettingsConfigDict(env_prefix="TEST_")


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Provide settings for tests."""
    return Settings()


__all__ = ["Settings", "settings"]
