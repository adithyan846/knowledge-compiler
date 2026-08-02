from pathlib import Path

import yaml


class IndexReader:

    def read(
        self,
        file: Path,
    ) -> dict:

        with file.open(
            "r",
            encoding="utf-8",
        ) as f:

            return yaml.safe_load(f) or {}
