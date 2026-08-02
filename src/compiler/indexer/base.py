"""
Base Indexer interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class Indexer(ABC):

    @abstractmethod
    def update(
        self,
        directory: Path,
    ) -> Path:
        """
        Build or update _index.yaml.

        Returns the generated index path.
        """
        raise NotImplementedError
