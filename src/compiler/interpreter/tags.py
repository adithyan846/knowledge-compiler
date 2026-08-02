"""
Tag interpreter – extracts relevant, clean keywords from multiple sources.
"""

from __future__ import annotations

import re
from typing import Set, Optional

from compiler.models import FragmentAnalysis
from compiler.interpreter.utils import clean_text


class TagInterpreter:
    # Stopwords (unchanged)
    STOPWORDS = { ... }  # keep as before

    MIN_WORD_LEN = 3
    MAX_TAG_LEN = 40
    MAX_HEADING_TAG_LEN = 30

    def interpret(self, analysis: FragmentAnalysis) -> list[str]:
        tags: Set[str] = set()

        # 1. Heading – clean and lower both words and whole heading
        if analysis.heading:
            heading = clean_text(analysis.heading)
            # Extract individual words (already lowercased in _extract_words)
            tags.update(self._extract_words(heading))
            # Add whole heading as a tag if short, but lower it
            if len(heading) <= self.MAX_HEADING_TAG_LEN and heading:
                tags.add(heading.lower())  # Ensure lowercase

        # 2. Technical terms – clean and lower
        for term in analysis.technical_terms:
            clean = self._clean_term(term)
            if clean:
                tags.add(clean)

        # 3. Parameters – clean and lower
        for param in analysis.parameters:
            clean = self._clean_term(param)
            if clean:
                tags.add(clean)

        # 4. Bullet points – extract key phrases (already lowercased by _extract_key_phrase)
        for bullet in analysis.bullet_points:
            bullet_clean = clean_text(bullet)
            phrase = self._extract_key_phrase(bullet_clean, max_words=3)
            if phrase:
                tags.add(phrase)

        # 5. Numbered steps – similar
        for step in analysis.numbered_steps:
            step_clean = clean_text(step)
            phrase = self._extract_key_phrase(step_clean, max_words=3)
            if phrase:
                tags.add(phrase)

        # 6. First sentences: add words overlapping with technical terms
        tech_words = set()
        for term in analysis.technical_terms:
            tech_words.update(term.lower().split())
        for sent in analysis.sentences[:2]:
            for word in self._extract_words(clean_text(sent)):
                if word in tech_words:
                    tags.add(word)

        # 7. Fallback: first paragraph
        if not tags and analysis.paragraphs:
            first_para = clean_text(analysis.paragraphs[0])
            for word in self._extract_words(first_para):
                tags.add(word)

        return sorted(tags)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _extract_words(self, text: str) -> Set[str]:
        words = re.findall(r'[A-Za-z0-9]+', text)
        cleaned = set()
        for w in words:
            w = w.lower()
            if len(w) >= self.MIN_WORD_LEN and w not in self.STOPWORDS:
                cleaned.add(w)
        return cleaned

    def _clean_term(self, term: str) -> str:
        term = term.lower().strip()
        term = re.sub(r'[^\w\s-]', '', term)
        term = re.sub(r'\s+', ' ', term).strip()
        if len(term) > self.MAX_TAG_LEN or len(term) < self.MIN_WORD_LEN:
            return ""
        if term in self.STOPWORDS:
            return ""
        return term

    def _extract_key_phrase(self, text: str, max_words: int = 3) -> Optional[str]:
        words = re.findall(r'[A-Za-z0-9]+', text)
        filtered = []
        for w in words:
            w = w.lower()
            if w not in self.STOPWORDS and len(w) >= self.MIN_WORD_LEN:
                filtered.append(w)
                if len(filtered) >= max_words:
                    break
        if filtered:
            phrase = " ".join(filtered)
            return phrase[:self.MAX_TAG_LEN]
        return None
