"""
compiler.extractor.simple

Simple knowledge extractor.

Removes obvious non-informational artefacts while preserving
engineering content.
"""

from __future__ import annotations

import re

from compiler.extractor.base import Extractor
from compiler.models import Document, KnowledgeCandidate


class SimpleExtractor(Extractor):
    """
    Conservative extractor.

    Performs only coarse cleaning.
    It does NOT split knowledge.
    """

    def extract(self, document: Document) -> KnowledgeCandidate:

        text = self._clean(document.text)

        return KnowledgeCandidate(
                document=document,
                text=text,
                start_line=1,
                end_line=text.count("\n") + 1,
                confidence=1.0,
                reason="Document cleaned and prepared for splitting."
            )
        

    def _clean(self, text: str) -> str:
        """
        Remove obvious formatting artefacts while preserving
        engineering information.
        """

        lines = []

        for line in text.splitlines():

            stripped = line.strip()

            # Remove empty repeated separators
            if re.fullmatch(r"[-=*_]{3,}", stripped):
                continue

            # Remove HTML comments
            if stripped.startswith("<!--") and stripped.endswith("-->"):
                continue

            # Remove common Markdown badges/images
            if stripped.startswith("!["):
                continue

            lines.append(line)

        cleaned = "\n".join(lines)

        # Collapse excessive blank lines
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

        return cleaned.strip()
