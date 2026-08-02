"""
Relation interpreter – generates candidate relation IDs from the fragment's own concepts.
"""

from __future__ import annotations

import re
from typing import Optional

from compiler.models import FragmentAnalysis


class RelationInterpreter:
    """
    Produce a list of concept‑based IDs derived from:
    - technical_terms
    - tags (computed via TagInterpreter, or from analysis.metadata)
    - parameters

    Each concept is slugified to a deterministic string like "concept_am32".
    These are intended to be resolved to actual KnowledgeUnit IDs by the Linker.
    """

    # Optional: external mapping from concept to real ID (injected or later)
    concept_to_id_map: Optional[dict[str, str]] = None

    def __init__(self, concept_map: Optional[dict[str, str]] = None) -> None:
        self.concept_to_id_map = concept_map or {}

    def interpret(self, analysis: FragmentAnalysis) -> list[str]:
        related_ids = set()

        # 1. Derive concepts from technical terms
        for term in analysis.technical_terms:
            concept_id = self._concept_id(term)
            if concept_id:
                related_ids.add(concept_id)

        # 2. Derive concepts from parameters
        for param in analysis.parameters:
            concept_id = self._concept_id(param)
            if concept_id:
                related_ids.add(concept_id)

        # 3. Derive concepts from tags (if available in metadata)
        if analysis.metadata and "tags" in analysis.metadata:
            for tag in analysis.metadata["tags"]:
                concept_id = self._concept_id(tag)
                if concept_id:
                    related_ids.add(concept_id)

        # 4. If we have an external map, resolve concept IDs to real IDs
        if self.concept_to_id_map:
            resolved = []
            for cid in related_ids:
                real_id = self.concept_to_id_map.get(cid)
                if real_id:
                    resolved.append(real_id)
            return resolved

        # Otherwise, return the concept IDs themselves (to be resolved later)
        return sorted(related_ids)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _concept_id(self, term: str) -> str:
        """Generate a deterministic concept ID from a term."""
        # Clean and slugify the term
        slug = re.sub(r'[^a-z0-9]+', '_', term.lower().strip())
        slug = re.sub(r'_+', '_', slug).strip('_')
        if not slug or len(slug) < 2:
            return ""
        return f"concept_{slug}"
