"""Run BM25 across all MERIT evaluation queries and save candidates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ml.baselines.bm25_retrieval import load_chunks, retrieve

QUERY_PATH = Path("ml/data/feasibility/evaluation_queries.jsonl")
CHUNK_PATH = Path("ml/data/feasibility/chunks/chunks.jsonl")
OUTPUT_PATH = Path("ml/data/feasibility/bm25_candidates.jsonl")

TOP_K = 5


def load_queries(path: Path) -> list[dict[str, str]]:
    """Load evaluation queries from JSONL."""
    queries: list[dict[str, str]] = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                queries.append(json.loads(line))

    return queries


def main() -> None:
    queries = load_queries(QUERY_PATH)
    records = load_chunks(CHUNK_PATH)

    output_records: list[dict[str, Any]] = []

    for query_record in queries:
        query_id = query_record["query_id"]
        query = query_record["query"]

        results = retrieve(
            query=query,
            records=records,
            top_k=TOP_K,
        )

        for rank, (chunk, score) in enumerate(
            results,
            start=1,
        ):
            output_records.append(
                {
                    "query_id": query_id,
                    "query": query,
                    "rank": rank,
                    "bm25_score": score,
                    "chunk_id": chunk["chunk_id"],
                    "document_id": chunk["document_id"],
                    "source_file": chunk["source_file"],
                    "page_number": chunk["page_number"],
                    "passage": chunk["text"],
                }
            )

        print(f"{query_id}: retrieved " f"{len(results)} candidates")

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for record in output_records:
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

    print()
    print(f"Queries processed: {len(queries)}")
    print(f"Candidates saved: {len(output_records)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
