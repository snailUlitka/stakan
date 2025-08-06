"""PDF parser, based on Docling (https://github.com/docling-project/docling)."""

from io import BytesIO

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.io import DocumentStream


class PDFParser:
    """Parser for PDF documents, based on Docling."""

    def __init__(self) -> None:
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True

        self._doc_converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            },
        )

    def parse(self, document: bytes) -> str:
        """Parse document bytes into `Document`."""
        result = self._doc_converter.convert(
            source=DocumentStream(name="", stream=BytesIO(document)),
        )

        return result.document.export_to_markdown()
