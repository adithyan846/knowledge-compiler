from __future__ import annotations

from pathlib import Path

import yaml

from compiler.schema.base import Schema


class SchemaLoader:

    def load(self, path: Path) -> Schema:

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if "version" not in data:
            raise ValueError(f"{path} is missing 'version'")

        if "id" not in data:
            raise ValueError(f"{path} is missing 'id'")

        return Schema(
            id=data["id"],
            name=data["name"],
            version=data["version"],
            extends=data.get("extends"),
            description=data.get("description"),
            required=data.get("required", []),
            optional=data.get("optional", []),
            field_definitions=data.get("field_definitions", {}),
            )

    def load_directory(
        self,
        directory: Path,
    ) -> dict[str, Schema]:

        schemas = {}

        for path in directory.glob("*.yaml"):

            schema = self.load(path)

            schemas[schema.id] = schema

        return schemas
