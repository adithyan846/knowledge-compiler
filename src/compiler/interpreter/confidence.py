"""
Confidence interpreter – computes a confidence score based on analysis richness.
"""

from __future__ import annotations

from compiler.models import FragmentAnalysis


class ConfidenceInterpreter:
    # Weights for different features
    WEIGHT_HEADING = 0.15
    WEIGHT_PARAGRAPHS = 0.15
    WEIGHT_SENTENCES = 0.10
    WEIGHT_BULLET_POINTS = 0.05
    WEIGHT_NUMBERED_STEPS = 0.05
    WEIGHT_CODE_BLOCKS = 0.05
    WEIGHT_TECHNICAL_TERMS = 0.10       # per term (capped at 3)
    WEIGHT_PARAMETERS = 0.10            # per term (capped at 3)
    WEIGHT_IMPERATIVE_VERBS = 0.05
    WEIGHT_COMMANDS = 0.05
    WEIGHT_URLS = 0.05
    WEIGHT_WORDS = 0.20                 # based on word count / 200 (capped)

    PENALTY_AMBIGUITY = 0.10
    MIN_CONFIDENCE = 0.20

    def interpret(self, analysis: FragmentAnalysis) -> float:
        score = 0.0

        # Structural completeness
        if analysis.heading:
            score += self.WEIGHT_HEADING
        if analysis.paragraphs:
            score += self.WEIGHT_PARAGRAPHS
        if analysis.sentences:
            score += self.WEIGHT_SENTENCES
        if analysis.bullet_points:
            score += self.WEIGHT_BULLET_POINTS
        if analysis.numbered_steps:
            score += self.WEIGHT_NUMBERED_STEPS
        if analysis.code_blocks:
            score += self.WEIGHT_CODE_BLOCKS

        # Semantic richness
        score += min(len(analysis.technical_terms), 3) * self.WEIGHT_TECHNICAL_TERMS
        score += min(len(analysis.parameters), 3) * self.WEIGHT_PARAMETERS
        if analysis.imperative_verbs:
            score += self.WEIGHT_IMPERATIVE_VERBS
        if analysis.commands:
            score += self.WEIGHT_COMMANDS
        if analysis.urls:
            score += self.WEIGHT_URLS

        # Content length: use analysis.words instead of raw text
        word_count = len(analysis.words) if analysis.words else 0
        score += min(word_count / 200.0, 1.0) * self.WEIGHT_WORDS

        # Penalties
        if analysis.metadata and "ambiguity_flags" in analysis.metadata:
            ambiguity_flags = analysis.metadata["ambiguity_flags"]
            score -= len(ambiguity_flags) * self.PENALTY_AMBIGUITY

        score = max(0.0, min(score, 1.0))
        if score < self.MIN_CONFIDENCE:
            score = self.MIN_CONFIDENCE
        return round(score, 3)
