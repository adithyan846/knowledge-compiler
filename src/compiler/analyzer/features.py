"""
Feature extraction.

Extract reusable semantic features.
"""

from __future__ import annotations

import re

from compiler.models import FragmentAnalysis


class FeatureAnalyzer:

    IMPERATIVE_VERBS = {
        "connect",
        "set",
        "configure",
        "install",
        "verify",
        "check",
        "enable",
        "disable",
        "run",
        "flash",
        "mount",
        "disconnect",
        "reboot",
        "restart",
        "copy",
        "move",
        "create",
        "delete",
    }

    WARNING_WORDS = {
        "warning",
        "danger",
        "caution",
        "always",
        "never",
        "important",
        "avoid",
    }

    COMMAND_PATTERN = re.compile(r"^\$|^sudo |^make |^git |^python ")

    PARAMETER_PATTERN = re.compile(
        r"\b[A-Z][A-Z0-9_]{2,}\b"
    )

    URL_PATTERN = re.compile(
        r"https?://\S+"
    )

    TECHNICAL_TERM_PATTERN = re.compile(
        r"\b[A-Za-z]+[0-9]+[A-Za-z0-9_-]*\b"
    )

    def analyze(
        self,
        analysis: FragmentAnalysis,
    ) -> None:

        text = analysis.fragment.text

        words = [word.lower() for word in analysis.words]

        analysis.imperative_verbs = [
            word
            for word in words
            if word in self.IMPERATIVE_VERBS
        ]

        analysis.warnings = [
            word
            for word in words
            if word in self.WARNING_WORDS
        ]

        analysis.parameters = self.PARAMETER_PATTERN.findall(text)

        analysis.urls = self.URL_PATTERN.findall(text)

        analysis.technical_terms = list(
            set(
                self.TECHNICAL_TERM_PATTERN.findall(text)
            )
        )

        analysis.commands = []

        for line in text.splitlines():

            stripped = line.strip()

            if self.COMMAND_PATTERN.match(stripped):

                analysis.commands.append(stripped)
