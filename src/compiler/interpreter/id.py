"""
Knowledge ID generator – produces deterministic, filesystem‑safe identifiers.
"""

from __future__ import annotations

import hashlib
import re

from compiler.interpreter.title import TitleInterpreter
from compiler.interpreter.utils import clean_text
from compiler.models import FragmentAnalysis


class IdInterpreter:
    MAX_ID_LENGTH = 100
    HASH_SUFFIX_LENGTH = 6

    def __init__(self) -> None:
        self.title_interpreter = TitleInterpreter()

    def interpret(self, analysis: FragmentAnalysis) -> str:
        base_title = self._get_base_title(analysis)
        slug = self._slugify(base_title)

        if not slug or slug == "untitled":
            slug = self._build_fallback_slug(analysis)

        hash_suffix = self._compute_suffix(analysis)
        if hash_suffix:
            combined = f"{slug}_{hash_suffix}"
        else:
            combined = slug

        if len(combined) > self.MAX_ID_LENGTH:
            combined = combined[:self.MAX_ID_LENGTH]
        return combined

    # ------------------------------------------------------------------
    # Core logic
    # ------------------------------------------------------------------

    def _get_base_title(self, analysis: FragmentAnalysis) -> str:
        title = self.title_interpreter.interpret(analysis)
        if title and title != "Untitled":
            return title

        # Fallback: use clean_text on heading, sentences, paragraphs
        if analysis.heading and analysis.heading.strip():
            return clean_text(analysis.heading)
        if analysis.sentences:
            return clean_text(analysis.sentences[0])
        if analysis.paragraphs:
            first = clean_text(analysis.paragraphs[0])
            if len(first) > 80:
                return first[:80] + "..."
            return first
        return "unknown"

    def _build_fallback_slug(self, analysis: FragmentAnalysis) -> str:
        parts = []
        if analysis.technical_terms:
            parts.extend(clean_text(t) for t in analysis.technical_terms[:3])
        if analysis.parameters:
            parts.extend(clean_text(p) for p in analysis.parameters[:2])
        if parts:
            # Remove empty strings
            parts = [p for p in parts if p]
            if parts:
                return "_".join(parts)[:self.MAX_ID_LENGTH]
        return "unknown"

    def _slugify(self, text: str) -> str:
        if not text:
            return "unknown"
        text = text.lower().strip()
        slug = re.sub(r'[^a-z0-9]+', '_', text)
        slug = re.sub(r'_+', '_', slug)
        return slug.strip('_') or "unknown"

    def _compute_suffix(self, analysis: FragmentAnalysis) -> str:
        # Use analysis.sentences (clean) instead of raw text
        if analysis.sentences:
            # Use first 200 chars from sentences
            text_sample = " ".join(analysis.sentences[:3])[:200].encode('utf-8')
            return hashlib.md5(text_sample).hexdigest()[:self.HASH_SUFFIX_LENGTH]
        elif analysis.paragraphs:
            text_sample = " ".join(analysis.paragraphs[:2])[:200].encode('utf-8')
            return hashlib.md5(text_sample).hexdigest()[:self.HASH_SUFFIX_LENGTH]
        return ""
