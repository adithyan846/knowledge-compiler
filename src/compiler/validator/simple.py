"""
Simple deterministic validator (schema‑driven, stateless).
"""

from __future__ import annotations

from compiler.validator.base import Validator
from compiler.validator.rules import (
    validate_content,
    validate_id,
    validate_summary,
    validate_tags,
    validate_title,
    validate_confidence,
    validate_related,
    validate_metadata,
    validate_unknown_types,
    validate_required_content_fields,
)
from compiler.models import KnowledgeUnit, ValidationResult
from compiler.schema.base import ResolvedSchema


class SimpleValidator(Validator):
    """
    Rule‑based validator that checks all KnowledgeUnit fields against a schema.

    The validator does not store any state; both unit and schema are passed
    to the validate() method. This makes it easy to reuse and test.

    If strict_mode is True, warnings are promoted to errors.
    """

    def __init__(self, strict_mode: bool = False) -> None:
        self.strict_mode = strict_mode

    def validate(self, unit: KnowledgeUnit, schema: ResolvedSchema) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        # Core field validators (generic)
        validate_id(errors, unit)
        validate_title(errors, unit)
        validate_summary(errors, warnings, unit)
        validate_tags(errors, warnings, unit)
        validate_content(errors, warnings, unit)
        validate_confidence(errors, warnings, unit)
        validate_related(errors, warnings, unit)
        validate_metadata(errors, unit)

        # Schema‑driven validation
        validate_unknown_types(warnings, schema)
        validate_required_content_fields(errors, unit, schema)

        # Strict mode
        if self.strict_mode:
            errors.extend(warnings)
            warnings = []

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )
