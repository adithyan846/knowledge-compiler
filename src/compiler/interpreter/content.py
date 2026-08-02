"""
Content interpreter – structures content from semantic observations.
No Markdown is copied into content fields.
"""

from __future__ import annotations

from compiler.models import FragmentAnalysis
from compiler.interpreter.types import TypeInterpreter
from compiler.interpreter.utils import clean_text


class ContentInterpreter:
    """
    Produce structured content based on the fragment's type.

    - workflow: steps (list) and commands (list)
    - fact: fact (first sentence)
    - troubleshooting: problem, cause, solution (strings)
    - reference: commands, urls, code_blocks (lists)
    - decision: options (list), criteria (list)
    - fallback: fact (first sentence)
    """

    TYPE_PRIORITY = ["workflow", "troubleshooting", "reference", "decision", "fact"]

    def __init__(self) -> None:
        self.type_interpreter = TypeInterpreter()

    def interpret(self, analysis: FragmentAnalysis) -> dict:
        types = self.type_interpreter.interpret(analysis)
        primary_type = self._select_primary_type(types)
        content = self._build_content(analysis, primary_type)

        # Keep raw text only as fallback (cleaned)
        content["text"] = clean_text(analysis.fragment.text) if analysis.fragment else ""
        return content

    def _select_primary_type(self, types: list[str]) -> str:
        for t in self.TYPE_PRIORITY:
            if t in types:
                return t
        return "fact"  # fallback

    def _build_content(self, analysis: FragmentAnalysis, primary_type: str) -> dict:
        if primary_type == "workflow":
            return self._build_workflow(analysis)
        elif primary_type == "troubleshooting":
            return self._build_troubleshooting(analysis)
        elif primary_type == "reference":
            return self._build_reference(analysis)
        elif primary_type == "decision":
            return self._build_decision(analysis)
        else:  # fact
            return self._build_fact(analysis)

    def _build_workflow(self, analysis: FragmentAnalysis) -> dict:
        steps = analysis.numbered_steps or analysis.bullet_points
        # Clean each step (remove Markdown, extra spaces)
        cleaned_steps = [clean_text(step) for step in steps if step.strip()]
        return {
            "steps": cleaned_steps,
            "commands": [clean_text(cmd) for cmd in analysis.commands],
        }

    def _build_troubleshooting(self, analysis: FragmentAnalysis) -> dict:
        problem = ""
        if analysis.warnings:
            problem = clean_text(analysis.warnings[0])
        elif analysis.sentences:
            problem = clean_text(analysis.sentences[0])

        # Simple cause extraction (first sentence with "caused by", "due to")
        cause = ""
        for para in analysis.paragraphs:
            lower = para.lower()
            if any(phrase in lower for phrase in ["caused by", "due to", "because"]):
                # Use the first sentence from that paragraph
                sentences = para.split('.')
                for sent in sentences:
                    if any(phrase in sent.lower() for phrase in ["caused by", "due to", "because"]):
                        cause = clean_text(sent)
                        break
                if cause:
                    break

        # Simple solution extraction (first bullet/paragraph with "solution", "fix", etc.)
        solution = ""
        for item in analysis.bullet_points + analysis.paragraphs:
            lower = item.lower()
            if any(kw in lower for kw in ["solution", "fix", "workaround", "resolve"]):
                solution = clean_text(item)
                break

        return {
            "problem": problem,
            "cause": cause,
            "solution": solution,
        }

    def _build_reference(self, analysis: FragmentAnalysis) -> dict:
        return {
            "commands": [clean_text(cmd) for cmd in analysis.commands],
            "urls": [clean_text(url) for url in analysis.urls],
            "code_blocks": [clean_text(block) for block in analysis.code_blocks],
        }

    def _build_decision(self, analysis: FragmentAnalysis) -> dict:
        options = analysis.bullet_points or analysis.numbered_steps
        cleaned_options = [clean_text(opt) for opt in options if opt.strip()]
        return {
            "options": cleaned_options,
            "criteria": [clean_text(c) for c in analysis.parameters],
        }

    def _build_fact(self, analysis: FragmentAnalysis) -> dict:
        fact = analysis.sentences[0] if analysis.sentences else analysis.fragment.text
        return {
            "fact": clean_text(fact),
            "parameters": [clean_text(p) for p in analysis.parameters],
            "technical_terms": [clean_text(t) for t in analysis.technical_terms],
        }
