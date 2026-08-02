"""
compiler.fragmenter.simple

Simple implementation of the Knowledge Fragmenter.

The fragmenter divides a KnowledgeCandidate into smaller,
structurally independent fragments.

It performs structural splitting only.
"""

from __future__ import annotations

from compiler.fragmenter.base import Fragmenter
from compiler.fragmenter.rules import is_markdown_heading
from compiler.models import (
    KnowledgeCandidate,
    KnowledgeFragment,
)


class SimpleFragmenter(Fragmenter):
    """
    Conservative fragmenter.

    Splits only at obvious structural boundaries such as
    Markdown headings.
    """

    def fragment(
        self,
        candidate: KnowledgeCandidate,
    ) -> list[KnowledgeFragment]:

        fragments: list[KnowledgeFragment] = []

        current_lines: list[str] = []

        fragment_start = 1

        lines = candidate.text.splitlines()

        for line_number, line in enumerate(lines, start=1):

            # Heading starts a new fragment
            if is_markdown_heading(line):

                # Save previous fragment
                if current_lines:
                    fragments.append(
                        KnowledgeFragment(
                            candidate=candidate,
                            text="\n".join(current_lines).strip(),
                            start_line=fragment_start,
                            end_line=line_number - 1,
                        )
                    )

                    current_lines = []

                fragment_start = line_number

            current_lines.append(line)

        # Save final fragment
        if current_lines:
            fragments.append(
                KnowledgeFragment(
                    candidate=candidate,
                    text="\n".join(current_lines).strip(),
                    start_line=fragment_start,
                    end_line=len(lines),
                )
            )

        return fragments
