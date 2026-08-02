"""
Structural analysis.
"""

from __future__ import annotations

import re

from compiler.models import FragmentAnalysis


class StructureAnalyzer:
    """
    Extract structural elements from a fragment.
    """

    def analyze(
        self,
        analysis: FragmentAnalysis,
    ) -> None:

        lines = analysis.fragment.text.splitlines()

        paragraph: list[str] = []

        for line in lines:

            stripped = line.strip()

            if not stripped:

                if paragraph:
                    analysis.paragraphs.append(
                        "\n".join(paragraph)
                    )
                    paragraph.clear()

                continue

            if stripped.startswith("#"):

                analysis.heading = stripped.lstrip("#").strip()

                continue

            if re.match(r"^[-*+]\s+", stripped):

                analysis.bullet_points.append(stripped)

                continue

            if re.match(r"^\d+[.)]\s+", stripped):

                analysis.numbered_steps.append(stripped)

                continue

            paragraph.append(stripped)

        if paragraph:

            analysis.paragraphs.append(
                "\n".join(paragraph)
            )
