"""Tests for recursive chunker."""

import re
from typing import Any

import pytest

from stakan.core.chunkers.recursive import Recursive


@pytest.fixture(
    params=[
        {"doc": "", "chunk_size": 10, "overlap": 2, "expected": [""]},
        {"doc": "short", "chunk_size": 10, "overlap": 2, "expected": ["short"]},
        {"doc": "abcdef", "chunk_size": 3, "overlap": 0, "expected": ["abc", "def"]},
        {
            "doc": "abcdef",
            "chunk_size": 3,
            "overlap": 1,
            "expected": ["abc", "cde", "ef"],
        },
    ]
)
def simple_cases(request: pytest.FixtureRequest) -> dict[str, Any]:
    return request.param


def test_simple_hard_split(simple_cases: dict[str, Any]):  # noqa: ANN201
    cfg = simple_cases
    r = Recursive(chunk_size=cfg["chunk_size"], overlap=cfg["overlap"])
    chunks = r.split(cfg["doc"])
    assert chunks == cfg["expected"]


@pytest.fixture(
    params=[
        {
            "doc": "X\n\nY\n\nZ",
            "chunk_size": 10,
            "overlap": 2,
            "expected": ["X\n\nY\n\nZ"],
        },
        {
            "doc": "a b c d",
            "chunk_size": 3,
            "overlap": 0,
            "expected": ["a b", "c d"],
        },
    ]
)
def sep_cases(request: pytest.FixtureRequest) -> dict[str, Any]:
    return request.param


def test_separator_splitting(sep_cases: dict[str, Any]):  # noqa: ANN201
    cfg = sep_cases
    r = Recursive(chunk_size=cfg["chunk_size"], overlap=cfg["overlap"])
    chunks = r.split(cfg["doc"])
    assert chunks == cfg["expected"]


@pytest.fixture(
    params=[
        {
            "doc": "abcdef",
            "chunk_size": 3,
            "overlap": -1,
            "expected": ["abc", "ef"],
        },
        {
            "doc": "any",
            "chunk_size": -1,
            "overlap": 1,
            "raises": ValueError,
        },
    ]
)
def edge_cases(request: pytest.FixtureRequest) -> dict[str, Any]:
    return request.param


def test_edge_parameters(edge_cases: dict[str, Any]):  # noqa: ANN201
    cfg = edge_cases
    r = Recursive(chunk_size=cfg["chunk_size"], overlap=cfg["overlap"])
    if "raises" in cfg:
        with pytest.raises(cfg["raises"]):
            r.split(cfg["doc"])
    else:
        chunks = r.split(cfg["doc"])
        assert chunks == cfg["expected"]


def test_zero_chunk_size_raises():  # noqa: ANN201
    msg = "Invalid split step: 0 (chunk_size=0, overlap=1)"
    with pytest.raises(ValueError, match=re.escape(msg)):
        Recursive(chunk_size=0, overlap=1).split("text")
