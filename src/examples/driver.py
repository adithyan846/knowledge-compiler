from pathlib import Path

from ..compiler.orchestrator.simple import SimpleOrchestrator


def main() -> None:

    compiler = SimpleOrchestrator()

    result = compiler.compile(
        source=Path("../compiler/sample.md"),
        output=Path("../../knowledge/drone/esc"),
    )

    print("\n" + "=" * 80)
    print("COMPILATION SUMMARY")
    print("=" * 80)

    print(f"Fragments : {result.fragments}")
    print(f"Written   : {result.written}")
    print(f"Failed    : {result.failed}")

    if result.warnings:
        print("\nWarnings")
        print("-" * 60)

        for warning in result.warnings:
            print(f"• {warning}")

    if result.files:
        print("\nGenerated Files")
        print("-" * 60)

        for file in result.files:
            print(file)

    print()


if __name__ == "__main__":
    main()
