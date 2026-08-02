"""
Simple rule-based interpreter.
"""

from __future__ import annotations

from compiler.interpreter.base import Interpreter

from compiler.interpreter.id import IdInterpreter
from compiler.interpreter.title import TitleInterpreter
from compiler.interpreter.summary import SummaryInterpreter
from compiler.interpreter.tags import TagInterpreter
from compiler.interpreter.types import TypeInterpreter
from compiler.interpreter.content import ContentInterpreter
from compiler.interpreter.relation import RelationInterpreter
from compiler.interpreter.confidence import ConfidenceInterpreter

from compiler.models import (
    FragmentAnalysis,
    KnowledgeUnit,
)


class SimpleInterpreter(Interpreter):

    def __init__(self) -> None:

        self.id = IdInterpreter()
        self.title = TitleInterpreter()
        self.summary = SummaryInterpreter()
        self.tags = TagInterpreter()
        self.types = TypeInterpreter()
        self.content = ContentInterpreter()
        self.relations = RelationInterpreter()
        self.confidence = ConfidenceInterpreter()

    def interpret(
        self,
        analysis: FragmentAnalysis,
    ) -> KnowledgeUnit:

        return KnowledgeUnit(
            id=self.id.interpret(analysis),
            title=self.title.interpret(analysis),
            summary=self.summary.interpret(analysis),
            tags=self.tags.interpret(analysis),
            types=self.types.interpret(analysis),
            content=self.content.interpret(analysis),
            related=self.relations.interpret(analysis),
            metadata={
                "confidence": self.confidence.interpret(analysis)
            },
        )
