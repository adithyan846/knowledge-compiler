"""
Base interface for knowledge interpreters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from compiler.models import (
    FragmentAnalysis,
    KnowledgeUnit,
)


class Interpreter(ABC):
    """
    Converts a FragmentAnalysis into a KnowledgeUnit.
    """

    @abstractmethod
    def interpret(
        self,
        analysis: FragmentAnalysis,
    ) -> KnowledgeUnit:
        raise NotImplementedError
