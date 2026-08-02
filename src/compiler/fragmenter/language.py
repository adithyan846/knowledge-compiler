"""
Language analysis.
"""

from __future__ import annotations

import re

from compiler.models import FragmentAnalysis


class LanguageAnalyzer:
    """
    Extract sentences and words.
    """

    def analyze(
        self,
        analysis: FragmentAnalysis,
    ) -> None:

        text = analysis.fragment.text

        analysis.sentences = [
            sentence.strip()
            for sentence in re.split(r"[.!?]\s+", text)
            if sentence.strip()
        ]

        analysis.words = re.findall(
            r"[A-Za-z0-9_./+-]+",
            text,
        )
