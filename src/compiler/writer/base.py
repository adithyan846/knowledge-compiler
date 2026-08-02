"""
Base writer interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from compiler.models import KnowledgeUnit
from compiler.schema.base import ResolvedSchema


class Writer(ABC):
    """
    Writes a validated KnowledgeUnit to disk.
    """

    @abstractmethod
    def write(
        self,
        unit: KnowledgeUnit,
        schema: ResolvedSchema,
        output_path: Path,
    ) -> Path:
        """
        Serialize a KnowledgeUnit.

        Returns the path of the generated file.
        """
        raise NotImplementedError
