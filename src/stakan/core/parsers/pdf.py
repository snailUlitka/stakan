"""PDF parser, based on Docling (https://github.com/docling-project/docling)."""

from docling.document_converter import DocumentConverter


class PDFParser:
    """Parser for PDF documents, based on Docling."""

    def parse(self, document: bytes) -> str:
        """Parse document bytes into `Document`."""
        # From docling docs: DocumentConverter().convert()
        raise NotImplementedError
