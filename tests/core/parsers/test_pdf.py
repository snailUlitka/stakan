"""Tests for PDF parser."""

import pytest

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
