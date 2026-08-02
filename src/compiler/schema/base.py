from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Schema:
    """
    One schema loaded from YAML.
    """
    id: str
    name: str
    version: int
    extends: str | None = None
    description: str | None = None
    required: list[str] = field(default_factory=list)
    optional: list[str] = field(default_factory=list)
    field_definitions: dict[str, dict] = field(default_factory=dict)


@dataclass(slots=True)
class ResolvedSchema:
    """
    Result after combining core + extensions.
    """
    schemas: list[str] = field(default_factory=list)   # IDs of the schemas merged
    required: set[str] = field(default_factory=set)
    optional: set[str] = field(default_factory=set)
    field_definitions: dict[str, dict] = field(default_factory=dict)
    unknown: list[str] = field(default_factory=list)
    version: int = 1
