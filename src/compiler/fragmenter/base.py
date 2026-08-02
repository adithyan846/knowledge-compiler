"""
compiler.fragmenter.base

Base interface for knowledge fragmenters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from compiler.models import KnowledgeCandidate, KnowledgeFragment


class Fragmenter(ABC):
    """
    Splits a KnowledgeCandidate into smaller structural fragments.

    A fragment is a coherent piece of text that can later be
    interpreted independently.
    """

    @abstractmethod
    def fragment(
        self,
        candidate: KnowledgeCandidate,
    ) -> list[KnowledgeFragment]:
        """
        Split a candidate into fragments.
        """
        raise NotImplementedError
