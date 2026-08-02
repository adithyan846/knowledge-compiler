"""
compiler.extractor.base

Base interface for knowledge extractors.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from compiler.models import Document, KnowledgeCandidate


class Extractor(ABC):
    """
    Base interface for all knowledge extractors.

    An extractor identifies candidate knowledge from a parsed
    Document. It does not classify, split, or validate knowledge.
    """

    @abstractmethod
    def extract(self, document: Document) -> KnowledgeCandidate:
        """
        Extract candidate knowledge from a Document.

        Parameters
        ----------
        document:
            Parsed document.

        Returns
        -------
        KnowledgeCandidate
            Candidate knowledge extracted from the document.
        """
        raise NotImplementedError
