"""
Convert a KnowledgeUnit into a YAML-ready dictionary.
"""

from __future__ import annotations

from compiler.models import KnowledgeUnit
from compiler.schema.base import ResolvedSchema


class YAMLBuilder:

    def build(
        self,
        unit: KnowledgeUnit,
        schema: ResolvedSchema,
    ) -> dict:

        data = {}

        # ----------------------------
        # Core schema
        # ----------------------------

        data["schema_version"] = schema.version 
        data["id"] = unit.id
        data["title"] = unit.title
        data["tags"] = unit.tags
        data["types"] = unit.types
        data["summary"] = unit.summary

        if unit.related:
            data["related"] = unit.related

        if unit.metadata:
            data["metadata"] = unit.metadata

        # ----------------------------
        # Type-specific fields
        # ----------------------------

        for field in sorted(schema.required | schema.optional):

            if field in data:
                continue

            if field in unit.content:
                data[field] = unit.content[field]

        return data
