"""
Simple rule-based analyzer.
"""

from __future__ import annotations

from compiler.analyzer.base import Analyzer

from compiler.analyzer.structure import StructureAnalyzer
from compiler.analyzer.language import LanguageAnalyzer
from compiler.analyzer.features import FeatureAnalyzer
from compiler.analyzer.statistics import StatisticsAnalyzer

from compiler.models import (
    FragmentAnalysis,
    KnowledgeFragment,
)


class SimpleAnalyzer(Analyzer):

    def __init__(self) -> None:

        self.structure = StructureAnalyzer()
        self.language = LanguageAnalyzer()
        self.features = FeatureAnalyzer()
        self.statistics = StatisticsAnalyzer()

    def analyze(
        self,
        fragment: KnowledgeFragment,
    ) -> FragmentAnalysis:

        analysis = FragmentAnalysis(fragment=fragment)

        self.structure.analyze(analysis)

        self.language.analyze(analysis)

        self.features.analyze(analysis)

        self.statistics.analyze(analysis)

        return analysis
