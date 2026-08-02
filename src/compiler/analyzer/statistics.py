"""
Statistics analysis.
"""

from __future__ import annotations

from compiler.models import FragmentAnalysis


class StatisticsAnalyzer:
    """
    Compute simple statistics used by later stages.
    """

    def analyze(
        self,
        analysis: FragmentAnalysis,
    ) -> None:

        stats = {}

        stats["characters"] = len(
            analysis.fragment.text
        )

        stats["lines"] = len(
            analysis.fragment.text.splitlines()
        )

        stats["words"] = len(
            analysis.words
        )

        stats["sentences"] = len(
            analysis.sentences
        )

        stats["paragraphs"] = len(
            analysis.paragraphs
        )

        stats["bullet_points"] = len(
            analysis.bullet_points
        )

        stats["numbered_steps"] = len(
            analysis.numbered_steps
        )

        stats["imperative_verbs"] = len(
            analysis.imperative_verbs
        )

        stats["parameters"] = len(
            analysis.parameters
        )

        stats["technical_terms"] = len(
            analysis.technical_terms
        )

        stats["warnings"] = len(
            analysis.warnings
        )

        stats["commands"] = len(
            analysis.commands
        )

        analysis.statistics = stats
