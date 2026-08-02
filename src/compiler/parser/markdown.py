"""
compiler.parser.markdown

Parser for Markdown documents.
"""

from pathlib import Path

from compiler.models import Document
from compiler.parser.base import Parser, DocumentSource

class MarkdownParser(Parser):
    """
    Parser for Markdown (.md) documents.
    """

    def parse(self, source: Path) -> Document:
        """
        Read a Markdown file and return a Document.
        """

        text = source.read_text(encoding="utf-8")

        return Document(
            source=DocumentSource.MARKDOWN,
            path=source,
            title=source.stem,
            text=text,
        )
