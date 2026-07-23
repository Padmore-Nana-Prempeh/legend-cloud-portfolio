"""BM25 retrieval baseline for the MERIT feasibility corpus."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from rank_bm25 import BM25Okapi

CHUNK_PATH = Path("ml/data/feasibility/chunks/chunks.jsonl")


def tokenize(text: str) -> list[str]:
    """Convert text into lowercase retrieval tokens."""
    return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())


def load_chunks(path: Path) -> list[dict[str, Any]]:
    """Load chunk records from JSONL."""
    if not path.exists():
        raise FileNotFoundError(f"Chunk file not found: {path}")

    records: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    return records


def retrieve(
    query: str,
    records: list[dict[str, Any]],
    top_k: int = 5,
) -> list[tuple[dict[str, Any], float]]:
    """Retrieve the highest-scoring chunks using BM25."""
    tokenized_corpus = [tokenize(record["text"]) for record in records]

    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = tokenize(query)

    scores = bm25.get_scores(tokenized_query)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda index: scores[index],
        reverse=True,
    )[:top_k]

    return [(records[index], float(scores[index])) for index in ranked_indices]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search the MERIT feasibility corpus with BM25."
    )

    parser.add_argument(
        "query",
        type=str,
        help="Natural-language search query.",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of chunks to retrieve.",
    )

    args = parser.parse_args()

    records = load_chunks(CHUNK_PATH)

    results = retrieve(
        query=args.query,
        records=records,
        top_k=args.top_k,
    )

    print(f"\nQuery: {args.query}")
    print(f"Corpus chunks: {len(records)}")
    print(f"Top K: {args.top_k}")
    print("=" * 80)

    for rank, (record, score) in enumerate(results, start=1):
        preview = record["text"][:350].replace("\n", " ")

        print(f"\nRank {rank}")
        print(f"Score: {score:.4f}")
        print(f"Document: {record['source_file']}")
        print(f"Page: {record['page_number']}")
        print(f"Chunk: {record['chunk_id']}")
        print(f"Text: {preview}...")


if __name__ == "__main__":
    main()
