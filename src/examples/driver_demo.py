from pathlib import Path

from compiler.parser.markdown import MarkdownParser
from compiler.extractor.simple import SimpleExtractor
from compiler.fragmenter.simple import SimpleFragmenter
from compiler.analyzer.simple import SimpleAnalyzer
from compiler.interpreter.simple import SimpleInterpreter
from compiler.validator.simple import SimpleValidator
from compiler.schema.loader import SchemaLoader
from compiler.schema.resolver import SchemaResolver


def print_stage(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main() -> None:

    path = Path("compiler/sample.md")

    parser = MarkdownParser()
    extractor = SimpleExtractor()
    fragmenter = SimpleFragmenter()
    analyzer = SimpleAnalyzer()
    interpreter = SimpleInterpreter()

    # Load schemas once (they are static)
    loader = SchemaLoader()
    schemas = loader.load_directory(Path("schema"))
    resolver = SchemaResolver(schemas)
    validator = SimpleValidator(strict_mode=False)

    # ------------------------------------------------------------------
    # Parse
    # ------------------------------------------------------------------

    document = parser.parse(path)

    print_stage("DOCUMENT")
    print(document.text)

    # ------------------------------------------------------------------
    # Extract
    # ------------------------------------------------------------------

    candidate = extractor.extract(document)

    print_stage("KNOWLEDGE CANDIDATE")
    print(candidate.text)

    # ------------------------------------------------------------------
    # Fragment
    # ------------------------------------------------------------------

    fragments = fragmenter.fragment(candidate)

    print_stage(f"KNOWLEDGE FRAGMENTS ({len(fragments)})")

    for i, fragment in enumerate(fragments, start=1):

        print(f"\nFragment {i}")
        print("-" * 60)
        print(f"Lines: {fragment.start_line} - {fragment.end_line}\n")
        print(fragment.text)

        # --------------------------------------------------------------
        # Analyze
        # --------------------------------------------------------------

        analysis = analyzer.analyze(fragment)

        print_stage(f"FRAGMENT ANALYSIS {i}")

        print(f"Heading          : {analysis.heading}")
        print(f"Paragraphs       : {len(analysis.paragraphs)}")
        print(f"Bullet Points    : {len(analysis.bullet_points)}")
        print(f"Numbered Steps   : {len(analysis.numbered_steps)}")
        print(f"Sentences        : {len(analysis.sentences)}")
        print(f"Words            : {len(analysis.words)}")

        print(f"\nImperative Verbs : {analysis.imperative_verbs}")
        print(f"Parameters       : {analysis.parameters}")
        print(f"Warnings         : {analysis.warnings}")
        print(f"Technical Terms  : {analysis.technical_terms}")
        print(f"Commands         : {analysis.commands}")
        print(f"URLs             : {analysis.urls}")

        print("\nStatistics")
        print("-" * 60)

        for key, value in analysis.statistics.items():
            print(f"{key:20}: {value}")

        # --------------------------------------------------------------
        # Interpret
        # --------------------------------------------------------------

        unit = interpreter.interpret(analysis)

        print_stage(f"KNOWLEDGE UNIT {i}")

        print(f"ID       : {unit.id}")
        print(f"Title    : {unit.title}")
        print(f"Summary  : {unit.summary}")
        print(f"Tags     : {unit.tags}")
        print(f"Types    : {unit.types}")
        print(f"Related  : {unit.related}")

        print("\nMetadata")
        print("-" * 60)
        print(unit.metadata)

        print("\nContent")
        print("-" * 60)
        print(unit.content)

        # --------------------------------------------------------------
        # Resolve schema and validate
        # --------------------------------------------------------------

        # 1. Resolve the schema for this unit's types
        resolved = resolver.resolve(unit.types)

        print_stage(f"RESOLVED SCHEMA {i}")

        print(f"Schemas used : {resolved.schemas}")
        print(f"Unknown types: {resolved.unknown}")

        print("\nRequired")
        print("-" * 60)
        for field in sorted(resolved.required):
            print(field)

        print("\nOptional")
        print("-" * 60)
        for field in sorted(resolved.optional):
            print(field)

        # 2. Instantiate validator with this schema (strict mode off for demo)
        unit = interpreter.interpret(analysis)
        resolved = resolver.resolve(unit.types)

        # 3. Validate the unit
        validation = validator.validate(unit, resolved)

        print_stage(f"VALIDATION {i}")

        print(f"Valid     : {validation.valid}")

        print("\nErrors")
        print("-" * 60)

        if validation.errors:
            for error in validation.errors:
                print(f"• {error}")
        else:
            print("None")

        print("\nWarnings")
        print("-" * 60)

        if validation.warnings:
            for warning in validation.warnings:
                print(f"• {warning}")
        else:
            print("None")


if __name__ == "__main__":
    main()
