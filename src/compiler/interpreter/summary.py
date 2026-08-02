"""
Summary interpreter – returns the first meaningful sentence.
"""

from __future__ import annotations

from compiler.models import FragmentAnalysis
from compiler.interpreter.utils import clean_text


class SummaryInterpreter:
    """
    Produce a summary consisting of the first meaningful sentence.
    No concatenation, no scoring, just clean text.
    """

    MIN_SENTENCE_LEN = 5

    def interpret(self, analysis: FragmentAnalysis) -> str:
        for sentence in analysis.sentences:
            cleaned = clean_text(sentence)
            if len(cleaned) >= self.MIN_SENTENCE_LEN:
                # Keep the period for summaries
                if sentence.strip().endswith("."):
                    cleaned += "."
                return cleaned

        # Fallback: first paragraph (cleaned)
        if analysis.paragraphs:
            first_para = clean_text(analysis.paragraphs[0])
            if first_para:
                # Truncate to a reasonable length if needed
                if len(first_para) > 200:
                    first_para = first_para[:200] + "..."
                return first_para

        return "No summary available."
