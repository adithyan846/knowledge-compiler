"""
compiler.models

Core data models used throughout the knowledge compiler.

Every stage of the compiler transforms one model into another.
These models are independent of YAML, databases, LLMs or storage.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass(slots=True)
class CompilationResult:

    fragments: int = 0

    written: int = 0

    failed: int = 0

    warnings: list[str] = field(default_factory=list)

    files: list[Path] = field(default_factory=list)


# ---------------------------------------------------------------------
# Stage 1
# ---------------------------------------------------------------------

@dataclass(slots=True)
class Document:
    """
    Raw input after parsing.

    Every parser (Markdown, PDF, ChatGPT, Terminal...)
    produces a Document.
    """

    source: str
    text: str

    path: Path | None = None
    title: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------
# Stage 2
# ---------------------------------------------------------------------

@dataclass(slots=True)
class KnowledgeCandidate:
    """
    A piece of text that may become knowledge.

    Candidates are extracted from a Document but have
    not yet been classified.
    """

    document: Document

    text: str

    start_line: int | None = None
    end_line: int | None = None
    confidence: float = 1.0

    reason: str | None = None

    context: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------
# Stage 3
# ---------------------------------------------------------------------

@dataclass(slots=True)
class KnowledgeFragment:
    """
    A structurally independent fragment extracted from a
    KnowledgeCandidate.

    Fragments preserve source information but have not yet
    been interpreted into structured knowledge.
    """

    candidate: KnowledgeCandidate

    text: str

    start_line: int | None = None
    end_line: int | None = None

    context: dict[str, Any] = field(default_factory=dict)
# ---------------------------------------------------------------------
# Stage 3+
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Stage 4
# ---------------------------------------------------------------------

@dataclass(slots=True)
class FragmentAnalysis:
    """
    Semantic analysis of a KnowledgeFragment.

    Produced once by the Analyzer and reused by every
    interpreter component.
    """

    fragment: KnowledgeFragment

    # -------------------------------------------------------------
    # Structure
    # -------------------------------------------------------------

    heading: str | None = None

    paragraphs: list[str] = field(default_factory=list)

    bullet_points: list[str] = field(default_factory=list)

    numbered_steps: list[str] = field(default_factory=list)

    code_blocks: list[str] = field(default_factory=list)

    # -------------------------------------------------------------
    # Language
    # -------------------------------------------------------------

    sentences: list[str] = field(default_factory=list)

    words: list[str] = field(default_factory=list)

    # -------------------------------------------------------------
    # Features
    # -------------------------------------------------------------

    imperative_verbs: list[str] = field(default_factory=list)

    technical_terms: list[str] = field(default_factory=list)

    parameters: list[str] = field(default_factory=list)

    urls: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    commands: list[str] = field(default_factory=list)

    # -------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------

    statistics: dict[str, int | float] = field(default_factory=dict)

    # -------------------------------------------------------------
    # Extensible
    # -------------------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)
# ---------------------------------------------------------------------
# Stage 4+
# ---------------------------------------------------------------------

@dataclass(slots=True)
class KnowledgeUnit:
    """
    Structured knowledge produced by the Interpreter.

    The unit is progressively enriched by later compiler stages
    (Linker, Validator and Writer) before being written to disk.
    """

    # -----------------------------------------------------------------
    # Core Schema
    # -----------------------------------------------------------------

    schema_version: int = 1

    id: str = ""

    title: str = ""

    summary: str = ""

    tags: list[str] = field(default_factory=list)

    types: list[str] = field(default_factory=list)

    # -----------------------------------------------------------------
    # Knowledge
    # -----------------------------------------------------------------

    content: dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------
    # Relationships
    # -----------------------------------------------------------------

    related: list[str] = field(default_factory=list)

    # -----------------------------------------------------------------
    # Compiler Metadata
    # -----------------------------------------------------------------

    confidence: float = 1.0

    source_fragment: KnowledgeFragment | None = None

    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

@dataclass(slots=True)
class ValidationResult:
    """
    Result returned by the schema validator.
    """

    valid: bool

    errors: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)
