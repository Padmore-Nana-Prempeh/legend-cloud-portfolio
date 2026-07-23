"""Load and validate MERIT relevance annotations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

VALID_RELEVANCE_LABELS = {0, 1, 2}


def load_annotations(path: Path) -> list[dict[str, Any]]:
    """Load JSONL annotations and validate the required schema."""
    if not path.exists():
        raise FileNotFoundError(f"Annotation file not found: {path}")

    records: list[dict[str, Any]] = []

    required_fields = {
        "query_id",
        "query",
        "document_id",
        "chunk_id",
        "passage",
        "relevance",
    }

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc

            missing = required_fields - record.keys()

            if missing:
                raise ValueError(
                    f"Line {line_number} missing fields: {sorted(missing)}"
                )

            if record["relevance"] not in VALID_RELEVANCE_LABELS:
                raise ValueError(
                    f"Line {line_number} has invalid relevance "
                    f"value {record['relevance']}. Expected 0, 1, or 2."
                )

            records.append(record)

    return records


if __name__ == "__main__":
    annotation_path = Path("ml/data/sample/relevance_annotations.jsonl")

    annotations = load_annotations(annotation_path)

    print(f"Loaded {len(annotations)} valid annotations.")

    for annotation in annotations:
        print(
            annotation["query_id"],
            annotation["chunk_id"],
            f"relevance={annotation['relevance']}",
        )
