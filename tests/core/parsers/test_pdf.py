"""Tests for PDF parser."""

import sys
import types
from unittest.mock import MagicMock

import pytest


# Provide minimal stubs for the optional ``docling`` dependency so that tests can
# run in environments where the real library is not installed. Only the pieces
# used by :class:`PDFParser` are implemented.
if "docling" not in sys.modules:  # pragma: no cover - executed only in tests
    docling = types.ModuleType("docling")
    sys.modules["docling"] = docling

    docling.datamodel = types.ModuleType("docling.datamodel")
    sys.modules["docling.datamodel"] = docling.datamodel

    base_models = types.ModuleType("docling.datamodel.base_models")
    class InputFormat:  # minimal enum-like container
        PDF = "PDF"
    base_models.InputFormat = InputFormat
    sys.modules["docling.datamodel.base_models"] = base_models

    pipeline_options_module = types.ModuleType("docling.datamodel.pipeline_options")
    class PdfPipelineOptions:
        def __init__(self) -> None:
            self.do_ocr = False
            self.do_table_structure = False
            self.table_structure_options = types.SimpleNamespace(
                do_cell_matching=False
            )
    pipeline_options_module.PdfPipelineOptions = PdfPipelineOptions
    sys.modules["docling.datamodel.pipeline_options"] = pipeline_options_module

    document_converter_module = types.ModuleType("docling.document_converter")
    class _DummyResult:
        def __init__(self, text: str) -> None:
            self.document = types.SimpleNamespace(
                export_to_markdown=lambda: text
            )

    class DocumentConverter:  # pragma: no cover - simple stub
        def __init__(self, *args, **kwargs) -> None:
            pass

        def convert(self, source) -> _DummyResult:  # noqa: D401 - stub
            """Return a result with static markdown."""
            return _DummyResult("## Heading 1\n\nThis is a simple PDF.")

    class PdfFormatOption:  # pragma: no cover - simple stub
        def __init__(self, pipeline_options=None) -> None:  # noqa: D401 - stub
            """Create format option."""
            self.pipeline_options = pipeline_options

    document_converter_module.DocumentConverter = DocumentConverter
    document_converter_module.PdfFormatOption = PdfFormatOption
    sys.modules["docling.document_converter"] = document_converter_module

    docling_core = types.ModuleType("docling_core")
    sys.modules["docling_core"] = docling_core
    docling_core.types = types.ModuleType("docling_core.types")
    sys.modules["docling_core.types"] = docling_core.types
    docling_core_types_io = types.ModuleType("docling_core.types.io")
    class DocumentStream:  # pragma: no cover - simple stub
        def __init__(self, name: str, stream) -> None:
            self.name = name
            self.stream = stream
    docling_core_types_io.DocumentStream = DocumentStream
    sys.modules["docling_core.types.io"] = docling_core_types_io

from docling.document_converter import DocumentConverter
from stakan.core.parsers.pdf import PDFParser


@pytest.fixture
def sample_pdf_bytes() -> bytes:
    return b"""%PDF-1.1
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200]
   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 73 >>
stream
BT
/F1 12 Tf 10 180 Td (Heading 1) Tj
10 -20 Td (This is a simple PDF.) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000150 00000 n
0000000225 00000 n
0000000340 00000 n
0000000460 00000 n
trailer
<< /Root 1 0 R /Size 6 >>
startxref
560
%%EOF
"""


@pytest.mark.unit
def test_parse(sample_pdf_bytes: bytes) -> None:
    parser = PDFParser()

    text = parser.parse(sample_pdf_bytes)

    assert text == "## Heading 1\n\nThis is a simple PDF."


@pytest.mark.unit
def test_pdf_converter_usage(sample_pdf_bytes: bytes, monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure ``PDFParser`` uses its internal converter once."""
    parser = PDFParser()

    # Track calls to the existing converter's ``convert`` method.
    original_convert = parser._doc_converter.convert
    convert_mock = MagicMock(wraps=original_convert)
    monkeypatch.setattr(parser._doc_converter, "convert", convert_mock)

    # Count any new ``DocumentConverter`` instantiations after parser creation.
    instantiation_count = 0
    original_init = DocumentConverter.__init__

    def tracking_init(self, *args, **kwargs):
        nonlocal instantiation_count
        instantiation_count += 1
        original_init(self, *args, **kwargs)

    monkeypatch.setattr(DocumentConverter, "__init__", tracking_init)

    parser.parse(sample_pdf_bytes)

    assert convert_mock.call_count == 1
    assert instantiation_count == 0
