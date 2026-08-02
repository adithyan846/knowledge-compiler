"""
compiler.parser.base

Base interface for all document parsers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeAlias
from enum import Enum

from compiler.models import Document

Source: TypeAlias = Path

class Parser(ABC):
    """
    Abstract base class for all document parsers.

    Every parser converts an input source into a Document.
    """

    @abstractmethod
    def parse(self, source: Source) -> Document:
        """
        Parse the given source and return a Document.

        Parameters
        ----------
        source:
            Path to the input document.

        Returns
        -------
        Document
            Parsed document.
        """
        raise NotImplementedError


class DocumentSource(str, Enum):
    MARKDOWN = "markdown"
    PDF = "pdf"
    CHATGPT = "chatgpt"
    TERMINAL = "terminal"
    REPOSITORY = "repository"
