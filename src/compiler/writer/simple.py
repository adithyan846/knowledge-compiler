"""
Simple YAML writer.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from compiler.writer.base import Writer
from compiler.writer.yaml_builder import YAMLBuilder

from compiler.models import KnowledgeUnit
from compiler.schema.base import ResolvedSchema


class SimpleWriter(Writer):

    def __init__(self) -> None:
        self.builder = YAMLBuilder()

    def write(
        self,
        unit: KnowledgeUnit,
        schema: ResolvedSchema,
        output_path: Path,
    ) -> Path:

        output_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = self.builder.build(
            unit,
            schema,
        )

        file_path = output_path / f"{unit.id}.yaml"

        with file_path.open(
            "w",
            encoding="utf-8",
        ) as f:

            yaml.safe_dump(
                data,
                f,
                sort_keys=False,
                default_flow_style=False,
                allow_unicode=True,
            )

        return file_path
