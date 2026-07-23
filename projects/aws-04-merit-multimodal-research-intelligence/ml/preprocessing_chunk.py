"""Chunk cleaned MERIT documents while preserving page metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path

INPUT_DIR = Path("ml/data/feasibility/cleaned")
OUTPUT_DIR = Path("ml/data/feasibility/chunks")

CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
MIN_CHUNK_LENGTH = 200


PAGE_PATTERN = re.compile(
    r"===== PAGE (\d+) =====\s*(.*?)(?=\n===== PAGE \d+ =====|\Z)",
    re.DOTALL,
)


def split_into_chunks(text: str) -> list[str]:
    """Split text into overlapping chunks near sentence boundaries."""
    chunks: list[str] = []

    start = 0
    text_length = len(text)

    while start < text_length:
        proposed_end = min(start + CHUNK_SIZE, text_length)

        if proposed_end < text_length:
            search_start = max(start, proposed_end - 200)
            boundary_region = text[search_start:proposed_end]

            sentence_boundaries = [
                boundary_region.rfind(". "),
                boundary_region.rfind("? "),
                boundary_region.rfind("! "),
            ]

            best_boundary = max(sentence_boundaries)

            if best_boundary != -1:
                end = search_start + best_boundary + 1
            else:
                end = proposed_end
        else:
            end = text_length

        chunk = text[start:end].strip()

        if len(chunk) >= MIN_CHUNK_LENGTH:
            chunks.append(chunk)

        if end == text_length:
            break

        next_start = max(0, end - CHUNK_OVERLAP)
        # Move the overlap start forward to the next word boundary
        # so a new chunk never begins in the middle of a word.

        if next_start > 0:
            next_space = text.find(" ", next_start)

            if next_space != -1 and next_space < end:
                next_start = next_space + 1

        if next_start <= start:
            next_start = end

        start = next_start

    return chunks


def process_document(path: Path) -> list[dict[str, object]]:
    """Create page-aware chunks for one cleaned document."""
    text = path.read_text(encoding="utf-8")

    document_id = path.stem.lower()
    document_id = re.sub(r"[^a-z0-9]+", "-", document_id).strip("-")

    records: list[dict[str, object]] = []

    page_matches = PAGE_PATTERN.findall(text)

    if not page_matches:
        raise ValueError(f"No page markers found in {path.name}")

    for page_number_text, page_text in page_matches:
        page_number = int(page_number_text)

        page_chunks = split_into_chunks(page_text)

        for chunk_index, chunk_text in enumerate(page_chunks, start=1):
            chunk_id = f"{document_id}-page{page_number}-chunk{chunk_index}"

            records.append(
                {
                    "chunk_id": chunk_id,
                    "document_id": document_id,
                    "source_file": path.name,
                    "page_number": page_number,
                    "chunk_index": chunk_index,
                    "text": chunk_text,
                    "character_count": len(chunk_text),
                }
            )

    return records


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_files = sorted(INPUT_DIR.glob("*.txt"))

    if not cleaned_files:
        raise FileNotFoundError(f"No cleaned text files found in {INPUT_DIR}")

    all_records: list[dict[str, object]] = []

    for path in cleaned_files:
        records = process_document(path)
        all_records.extend(records)

        print(f"{path.name}: {len(records)} chunks")

    output_path = OUTPUT_DIR / "chunks.jsonl"

    with output_path.open("w", encoding="utf-8") as file:
        for record in all_records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    print()
    print(f"Total chunks: {len(all_records)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
