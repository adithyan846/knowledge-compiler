from pathlib import Path

import yaml

from compiler.indexer.base import Indexer
from compiler.indexer.builder import IndexBuilder


class SimpleIndexer(Indexer):

    def __init__(self):

        self.builder = IndexBuilder()

    def update(
        self,
        directory: Path,
    ) -> Path:

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        index = self.builder.build(directory)

        output = directory / "_index.yaml"

        with output.open(
            "w",
            encoding="utf-8",
        ) as f:

            yaml.safe_dump(
                index,
                f,
                sort_keys=False,
                allow_unicode=True,
            )

        return output
