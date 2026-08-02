from __future__ import annotations
from abc import ABC, abstractmethod
from compiler.models import KnowledgeUnit, ValidationResult
from compiler.schema.base import ResolvedSchema   # add import

class Validator(ABC):
    @abstractmethod
    def validate(self, unit: KnowledgeUnit, schema: ResolvedSchema) -> ValidationResult:
        raise NotImplementedError
