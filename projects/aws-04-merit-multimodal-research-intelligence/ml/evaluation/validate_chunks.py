"""Validate the MERIT feasibility chunk corpus."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CHUNK_PATH = Path("ml/data/feasibility/chunks/chunks.jsonl")

REQUIRED_FIELDS = {
    "chunk_id",
    "document_id",
    "source_file",
    "page_number",
    "chunk_index",
    "text",
    "character_count",
}


def load_chunks(path: Path) -> list[dict[str, Any]]:
    """Load and validate chunk records."""
    if not path.exists():
        raise FileNotFoundError(f"Chunk file not found: {path}")

    records: list[dict[str, Any]] = []
    chunk_ids: set[str] = set()

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            record = json.loads(line)

            missing_fields = REQUIRED_FIELDS - record.keys()

            if missing_fields:
                raise ValueError(
                    f"Line {line_number} missing fields: " f"{sorted(missing_fields)}"
                )

            chunk_id = record["chunk_id"]

            if chunk_id in chunk_ids:
                raise ValueError(f"Duplicate chunk_id found: {chunk_id}")

            if not record["text"].strip():
                raise ValueError(f"Empty text found for chunk: {chunk_id}")

            if record["character_count"] != len(record["text"]):
                raise ValueError(f"Character count mismatch for: {chunk_id}")

            if record["page_number"] < 1:
                raise ValueError(f"Invalid page number for: {chunk_id}")

            chunk_ids.add(chunk_id)
            records.append(record)

    return records


def main() -> None:
    records = load_chunks(CHUNK_PATH)

    document_ids = {record["document_id"] for record in records}

    character_counts = [record["character_count"] for record in records]

    print(f"Valid chunks: {len(records)}")
    print(f"Documents: {len(document_ids)}")
    print(f"Minimum chunk size: {min(character_counts)}")
    print(f"Maximum chunk size: {max(character_counts)}")
    print(
        f"Average chunk size: " f"{sum(character_counts) / len(character_counts):.1f}"
    )
    print("Chunk corpus validation passed.")


if __name__ == "__main__":
    main()
