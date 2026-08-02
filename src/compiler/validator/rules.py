"""
Validation rules for KnowledgeUnit (generic, schema‑driven).
"""

from __future__ import annotations

import re
from typing import List

from compiler.models import KnowledgeUnit 
from compiler.schema.base import ResolvedSchema

# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

ID_PATTERN = re.compile(r"^[a-z0-9_\-\.]+$")
MAX_TAGS = 20

# ---------------------------------------------------------------------
# Core validation functions (no type knowledge)
# ---------------------------------------------------------------------

def validate_id(errors: List[str], unit: KnowledgeUnit) -> None:
    if not hasattr(unit, "id") or unit.id is None:
        errors.append("Missing knowledge id.")
        return
    if not isinstance(unit.id, str):
        errors.append("Knowledge id must be a string.")
        return
    if not unit.id.strip():
        errors.append("Knowledge id is empty.")
        return
    if not ID_PATTERN.fullmatch(unit.id):
        errors.append(f"Invalid knowledge id '{unit.id}'. Use only a-z, 0-9, '_', '-', '.'.")


def validate_title(errors: List[str], unit: KnowledgeUnit) -> None:
    if not hasattr(unit, "title") or unit.title is None:
        errors.append("Missing title.")
        return
    if not isinstance(unit.title, str):
        errors.append("Title must be a string.")
        return
    if not unit.title.strip():
        errors.append("Title is empty.")


def validate_summary(errors: List[str], warnings: List[str], unit: KnowledgeUnit) -> None:
    if not hasattr(unit, "summary") or unit.summary is None:
        warnings.append("Summary is missing.")
        return
    if not isinstance(unit.summary, str):
        errors.append("Summary must be a string.")
        return
    if not unit.summary.strip():
        warnings.append("Summary is empty.")


def validate_tags(errors: List[str], warnings: List[str], unit: KnowledgeUnit) -> None:
    if not hasattr(unit, "tags") or unit.tags is None:
        errors.append("Missing tags list.")
        return
    if not isinstance(unit.tags, list):
        errors.append("Tags must be a list.")
        return
    if not unit.tags:
        warnings.append("No tags found.")
        return
    for i, tag in enumerate(unit.tags):
        if not isinstance(tag, str):
            errors.append(f"Tag at index {i} is not a string: {tag!r}")
        elif not tag.strip():
            errors.append(f"Tag at index {i} is empty.")
        elif len(tag) > 50:
            warnings.append(f"Tag '{tag}' exceeds 50 characters.")
    seen = set()
    duplicates = []
    for tag in unit.tags:
        if tag in seen:
            duplicates.append(tag)
        else:
            seen.add(tag)
    if duplicates:
        warnings.append(f"Duplicate tags detected: {duplicates}")
    if len(unit.tags) > MAX_TAGS:
        warnings.append(f"More than {MAX_TAGS} tags ({len(unit.tags)}) - consider pruning.")


def validate_content(errors: List[str], warnings: List[str], unit: KnowledgeUnit) -> None:
    if not hasattr(unit, "content") or unit.content is None:
        errors.append("Content is missing.")
        return
    if not isinstance(unit.content, dict):
        errors.append("Content must be a dictionary.")
        return
    if "text" not in unit.content:
        errors.append("Content missing required key: 'text'.")
    else:
        text = unit.content["text"]
        if not isinstance(text, str):
            errors.append("content['text'] must be a string.")
        elif not text.strip():
            warnings.append("content['text'] is empty.")


def validate_confidence(errors: List[str], warnings: List[str], unit: KnowledgeUnit) -> None:
    if not hasattr(unit, "confidence") or unit.confidence is None:
        warnings.append("Confidence is missing (will default to 1.0).")
        return
    if not isinstance(unit.confidence, (int, float)):
        errors.append("Confidence must be a number.")
        return
    if not (0.0 <= unit.confidence <= 1.0):
        errors.append("Confidence must be between 0.0 and 1.0.")


def validate_related(errors: List[str], warnings: List[str], unit: KnowledgeUnit) -> None:
    if not hasattr(unit, "related") or unit.related is None:
        return  # optional
    if not isinstance(unit.related, list):
        errors.append("Related must be a list.")
        return
    if unit.related:
        for i, rid in enumerate(unit.related):
            if not isinstance(rid, str):
                errors.append(f"Related ID at index {i} is not a string: {rid!r}")
            elif not rid.strip():
                errors.append(f"Related ID at index {i} is empty.")


def validate_metadata(errors: List[str], unit: KnowledgeUnit) -> None:
    if hasattr(unit, "metadata") and unit.metadata is not None:
        if not isinstance(unit.metadata, dict):
            errors.append("Metadata must be a dictionary.")


# ---------------------------------------------------------------------
# Schema‑driven validation (replaces type‑specific checks)
# ---------------------------------------------------------------------

def validate_unknown_types(
    warnings: List[str],
    schema: ResolvedSchema,
) -> None:
    """
    Emit warnings for any types that could not be resolved.
    """
    if schema.unknown:
        warnings.append(f"Unknown schema types: {schema.unknown}")


def validate_required_content_fields(
    errors: List[str],
    unit: KnowledgeUnit,
    schema: ResolvedSchema,
) -> None:
    """
    Ensure that all required content fields (from schema) are present.
    Skip core fields (already validated separately) to avoid duplication.
    """
    core_fields = {"schema_version", "id", "title", "summary", "tags", "types", "related", "metadata", "confidence"}
    for field in schema.required:
        if field in core_fields:
            continue
        if field not in unit.content:
            errors.append(f"Missing required content field '{field}'.")
