from __future__ import annotations

from compiler.schema.base import (
    Schema,
    ResolvedSchema,
)


class SchemaResolver:

    def __init__(
        self,
        schemas: dict[str, Schema],
    ):
        self.schemas = schemas

    def resolve(
        self,
        types: list[str],
    ) -> ResolvedSchema:

        resolved = ResolvedSchema()
        merged_ids = []

        # Always include core
        if "core" in self.schemas:
            self._merge_with_extensions(resolved, "core", merged_ids)
        else:
            # If no core, we just continue but may miss required fields
            pass

        # Merge requested types
        for schema_name in types:
            if schema_name not in self.schemas:
                resolved.unknown.append(schema_name)
                continue
            if schema_name not in merged_ids:
                self._merge_with_extensions(resolved, schema_name, merged_ids)

        # Set the list of schemas used
        resolved.schemas = merged_ids

        return resolved

    def _merge_with_extensions(
        self,
        resolved: ResolvedSchema,
        schema_name: str,
        merged_ids: list[str],
    ) -> None:
        """
        Merge a schema and its extensions (depth-first, pre-order).
        """
        schema = self.schemas[schema_name]

        # Merge extensions first
        if schema.extends and schema.extends not in merged_ids:
            self._merge_with_extensions(resolved, schema.extends, merged_ids)

        # Merge this schema
        self._merge(resolved, schema)
        merged_ids.append(schema_name)

    def _merge(
        self,
        resolved: ResolvedSchema,
        schema: Schema,
    ) -> None:
        resolved.required.update(schema.required)
        resolved.optional.update(schema.optional)
        resolved.field_definitions.update(schema.field_definitions)
