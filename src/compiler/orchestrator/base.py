"""
Base compiler orchestrator.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class Orchestrator(ABC):

    @abstractmethod
    def compile(
        self,
        source: Path,
        output: Path,
    ) -> None:
        """
        Compile a source document into knowledge files.
        """
        raise NotImplementedError
