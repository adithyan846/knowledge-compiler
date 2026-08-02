"""
Fragmentation rules.

The Fragmenter uses these rules to determine where a new
KnowledgeFragment should begin.

Rules are intentionally deterministic and conservative.
"""

from __future__ import annotations

import re


HEADING_PATTERNS = [
    re.compile(r"^#{1,6}\s"),          # Markdown headings
    re.compile(r"^.+\n[=-]{3,}$"),     # Setext headings (future)
]


def is_markdown_heading(line: str) -> bool:
    """Return True if the line is a Markdown heading."""
    return bool(re.match(r"^#{1,6}\s", line))


def is_horizontal_rule(line: str) -> bool:
    """Return True for markdown horizontal rules."""
    return bool(re.fullmatch(r"[-*_]{3,}", line.strip()))
