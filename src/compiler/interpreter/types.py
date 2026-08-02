"""
Knowledge type interpreter – heuristic classification using multiple signals.
Only emits types that have schemas (workflow, fact, troubleshooting, reference, decision).
"""

from __future__ import annotations

from compiler.models import FragmentAnalysis


class TypeInterpreter:
    """
    Classify a fragment into one or more types (workflow, fact, troubleshooting,
    reference, decision) based on scoring rules.

    Every type with a score above the threshold is returned.
    If none qualify, "fact" is returned as a fallback.
    """

    THRESHOLD = 2.0

    WEIGHTS = {
        "fact": {
            "parameters": 2.0,
            "technical_terms": 1.0,
            "parameter_assignments": 1.5,
        },
        "workflow": {
            "imperative_verbs": 2.0,
            "numbered_steps": 3.0,
            "bullet_points": 1.0,
            "commands": 1.0,
        },
        "troubleshooting": {
            "warnings": 3.0,
            "causes": 2.0,
            "solutions": 2.0,
        },
        "reference": {
            "commands": 2.0,
            "urls": 2.0,
            "code_blocks": 1.5,
            "technical_terms": 0.5,
        },
        "decision": {
            "decision_keywords": 3.0,
            "imperative_verbs": 1.0,
            "parameters": 0.5,
        },
    }

    def interpret(self, analysis: FragmentAnalysis) -> list[str]:
        scores = self._compute_scores(analysis)
        selected = [t for t, s in scores.items() if s >= self.THRESHOLD]
        if not selected:
            selected.append("fact")
        return sorted(selected)

    def _compute_scores(self, analysis: FragmentAnalysis) -> dict[str, float]:
        scores = {t: 0.0 for t in self.WEIGHTS}

        # ---- Fact ----
        scores["fact"] += self.WEIGHTS["fact"]["parameters"] * len(analysis.parameters)
        scores["fact"] += self.WEIGHTS["fact"]["technical_terms"] * min(len(analysis.technical_terms), 3)
        # Detect parameter assignments: "=" or ":" in text
        if analysis.paragraphs:
            for para in analysis.paragraphs:
                if "=" in para or ":" in para:
                    scores["fact"] += self.WEIGHTS["fact"]["parameter_assignments"]
                    break

        # ---- Workflow ----
        scores["workflow"] += self.WEIGHTS["workflow"]["imperative_verbs"] * min(len(analysis.imperative_verbs), 2)
        scores["workflow"] += self.WEIGHTS["workflow"]["numbered_steps"] * min(len(analysis.numbered_steps), 3)
        scores["workflow"] += self.WEIGHTS["workflow"]["bullet_points"] * min(len(analysis.bullet_points), 2)
        if analysis.commands:
            scores["workflow"] += self.WEIGHTS["workflow"]["commands"] * min(len(analysis.commands), 2)

        # ---- Troubleshooting ----
        scores["troubleshooting"] += self.WEIGHTS["troubleshooting"]["warnings"] * min(len(analysis.warnings), 2)
        # Detect cause phrases
        cause_phrases = ["caused by", "due to", "because", "result of"]
        if analysis.paragraphs:
            for para in analysis.paragraphs:
                if any(p in para.lower() for p in cause_phrases):
                    scores["troubleshooting"] += self.WEIGHTS["troubleshooting"]["causes"]
                    break
        # Detect solution phrases
        solution_phrases = ["solution", "fix", "workaround", "resolve"]
        if analysis.heading and any(p in analysis.heading.lower() for p in solution_phrases):
            scores["troubleshooting"] += self.WEIGHTS["troubleshooting"]["solutions"]
        if analysis.paragraphs and any(
            any(p in para.lower() for p in solution_phrases) for para in analysis.paragraphs
        ):
            scores["troubleshooting"] += self.WEIGHTS["troubleshooting"]["solutions"] * 0.5

        # ---- Reference ----
        scores["reference"] += self.WEIGHTS["reference"]["commands"] * min(len(analysis.commands), 2)
        scores["reference"] += self.WEIGHTS["reference"]["urls"] * min(len(analysis.urls), 2)
        scores["reference"] += self.WEIGHTS["reference"]["code_blocks"] * min(len(analysis.code_blocks), 2)
        if analysis.technical_terms:
            scores["reference"] += self.WEIGHTS["reference"]["technical_terms"] * min(len(analysis.technical_terms), 2)

        # ---- Decision ----
        decision_keywords = ["decision", "choose", "select", "decide", "option", "alternative"]
        if analysis.heading:
            heading_lower = analysis.heading.lower()
            for kw in decision_keywords:
                if kw in heading_lower:
                    scores["decision"] += self.WEIGHTS["decision"]["decision_keywords"]
                    break
        scores["decision"] += self.WEIGHTS["decision"]["imperative_verbs"] * min(len(analysis.imperative_verbs), 2)
        if analysis.parameters:
            scores["decision"] += self.WEIGHTS["decision"]["parameters"] * min(len(analysis.parameters), 2)

        # Cap scores
        for t in scores:
            scores[t] = min(scores[t], 10.0)

        return scores
