from __future__ import annotations

from pathlib import Path

from compiler.models import (
    CompilationResult,
    KnowledgeFragment,
)

from compiler.orchestrator.base import Orchestrator

from compiler.parser.markdown import MarkdownParser
from compiler.extractor.simple import SimpleExtractor
from compiler.fragmenter.simple import SimpleFragmenter
from compiler.analyzer.simple import SimpleAnalyzer
from compiler.interpreter.simple import SimpleInterpreter

from compiler.schema.loader import SchemaLoader
from compiler.schema.resolver import SchemaResolver

from compiler.validator.simple import SimpleValidator
from compiler.writer.simple import SimpleWriter
from compiler.indexer.simple import SimpleIndexer


class SimpleOrchestrator(Orchestrator):

    def __init__(
        self,
        schema_directory: Path = Path("schema"),
    ) -> None:

        self.parser = MarkdownParser()
        self.extractor = SimpleExtractor()
        self.fragmenter = SimpleFragmenter()
        self.analyzer = SimpleAnalyzer()
        self.interpreter = SimpleInterpreter()

        loader = SchemaLoader()
        schemas = loader.load_directory(schema_directory)
        self.resolver = SchemaResolver(schemas)

        self.validator = SimpleValidator()

        self.writer = SimpleWriter()

        self.indexer = SimpleIndexer()

    def _compile_fragment(
        self,
        fragment: KnowledgeFragment,
        output: Path,
    ) -> tuple[Path | None, list[str]]:

        analysis = self.analyzer.analyze(fragment)

        unit = self.interpreter.interpret(analysis)

        schema = self.resolver.resolve(unit.types)

        validation = self.validator.validate(
            unit,
            schema,
        )

        if not validation.valid:
            return None, validation.errors

        written = self.writer.write(
            unit,
            schema,
            output,
        )

        return written, validation.warnings

    def compile(
        self,
        source: Path,
        output: Path,
    ) -> CompilationResult:

        result = CompilationResult()

        document = self.parser.parse(source)

        candidate = self.extractor.extract(document)

        fragments = self.fragmenter.fragment(candidate)

        result.fragments = len(fragments)

        for fragment in fragments:

            written, warnings = self._compile_fragment(
                fragment,
                output,
            )

            result.warnings.extend(warnings)

            if written is None:
                result.failed += 1
                continue

            result.written += 1
            result.files.append(written)

        if result.written > 0:
            self.indexer.update(output)

        return result
