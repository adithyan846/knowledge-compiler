"""
Base interface for fragment analyzers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from compiler.models import (
    FragmentAnalysis,
    KnowledgeFragment,
)


class Analyzer(ABC):
    """
    Analyzes a KnowledgeFragment and produces a reusable
    FragmentAnalysis.
    """

    @abstractmethod
    def analyze(
        self,
        fragment: KnowledgeFragment,
    ) -> FragmentAnalysis:
        raise NotImplementedError
