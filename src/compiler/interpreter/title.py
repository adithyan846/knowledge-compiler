"""
Deterministic title interpreter with priority-based selection.
"""

from __future__ import annotations

from typing import List
from compiler.models import FragmentAnalysis
from compiler.interpreter.utils import clean_text


class TitleInterpreter:
    """
    Generate a descriptive title using deterministic priority:

    1. First meaningful sentence (≥ MIN_TITLE_LEN chars)
    2. Constructed title from terms (if fragment looks like a workflow)
    3. Heading (if present and not generic)
    4. Truncated first paragraph
    5. Fallback: "Untitled"
    """

    MIN_TITLE_LEN = 5
    MAX_TITLE_LEN = 100
    GENERIC_HEADINGS = {"introduction", "overview", "summary", "notes", "misc"}

    def interpret(self, analysis: FragmentAnalysis) -> str:
        # 1. First meaningful sentence
        sentence = self._first_meaningful_sentence(analysis)
        if sentence:
            return sentence

        # 2. Constructed title (only if fragment looks like a workflow)
        if self._is_workflow(analysis):
            constructed = self._build_from_terms(
                analysis.technical_terms,
                analysis.parameters,
                analysis.imperative_verbs,
            )
            if constructed:
                return constructed

        # 3. Heading (if present and not generic)
        if analysis.heading:
            heading = clean_text(analysis.heading)
            if heading and heading.lower() not in self.GENERIC_HEADINGS:
                return heading

        # 4. Fallback: first paragraph truncated
        if analysis.paragraphs:
            para = analysis.paragraphs[0].strip()
            if para:
                short = clean_text(para)[:self.MAX_TITLE_LEN]
                if len(para) > self.MAX_TITLE_LEN:
                    short += "..."
                return short

        return "Untitled"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _first_meaningful_sentence(self, analysis: FragmentAnalysis) -> str:
        for sentence in analysis.sentences:
            cleaned = clean_text(sentence)
            if len(cleaned) >= self.MIN_TITLE_LEN:
                return cleaned
        return ""

    def _is_workflow(self, analysis: FragmentAnalysis) -> bool:
        return bool(analysis.imperative_verbs) or bool(analysis.numbered_steps)

    def _build_from_terms(self, terms: List[str], params: List[str], verbs: List[str]) -> str:
        if verbs:
            verb = verbs[0].capitalize()
        else:
            verb = "Configure"
        if params:
            return f"{verb} {params[0]}"
        if terms:
            return f"{verb} {terms[0]}"
        return ""
