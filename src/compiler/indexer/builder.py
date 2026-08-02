from pathlib import Path

from compiler.indexer.reader import IndexReader


class IndexBuilder:

    def __init__(self):

        self.reader = IndexReader()

    def build(
        self,
        directory: Path,
    ) -> dict:

        entries = []

        for file in sorted(directory.glob("*.yaml")):

            if file.name == "_index.yaml":
                continue

            data = self.reader.read(file)

            entries.append(
                {
                    "id": data.get("id"),
                    "title": data.get("title"),
                    "summary": data.get("summary"),
                    "tags": data.get("tags", []),
                    "types": data.get("types", []),
                    "file": file.name,
                }
            )

        return {
            "version": 1,
            "knowledge": entries,
        }
