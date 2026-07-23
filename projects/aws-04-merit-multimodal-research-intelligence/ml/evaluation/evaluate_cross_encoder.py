import json
import math
import time
from collections import defaultdict
from pathlib import Path

import torch
from sentence_transformers import CrossEncoder

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

ANNOTATIONS = Path("ml/data/feasibility/relevance_annotations.jsonl")


def dcg(relevances):
    total = 0.0

    for index, relevance in enumerate(relevances, start=1):
        total += (2**relevance - 1) / math.log2(index + 1)

    return total


def ndcg_at_k(relevances, k):
    actual = relevances[:k]
    ideal = sorted(relevances, reverse=True)[:k]

    ideal_score = dcg(ideal)

    if ideal_score == 0:
        return 0.0

    return dcg(actual) / ideal_score


def precision_at_k(relevances, k):
    selected = relevances[:k]

    if not selected:
        return 0.0

    relevant = sum(rel > 0 for rel in selected)

    return relevant / k


def reciprocal_rank(relevances):
    for rank, relevance in enumerate(relevances, start=1):
        if relevance > 0:
            return 1.0 / rank

    return 0.0


records_by_query = defaultdict(list)

with ANNOTATIONS.open("r", encoding="utf-8") as f:
    for line in f:
        record = json.loads(line)
        records_by_query[record["query_id"]].append(record)


device = "mps" if torch.backends.mps.is_available() else "cpu"

print("=" * 72)
print("MERIT CROSS-ENCODER FEASIBILITY EVALUATION")
print("=" * 72)

print(f"Model: {MODEL_NAME}")
print(f"Device: {device}")

print("\nLoading model...")

load_start = time.perf_counter()

model = CrossEncoder(
    MODEL_NAME,
    device=device,
)

load_seconds = time.perf_counter() - load_start

print(f"Model loaded in {load_seconds:.2f} seconds")


metrics = {
    "precision@1": [],
    "precision@3": [],
    "precision@5": [],
    "mrr": [],
    "ndcg@5": [],
    "direct_answer_recall@5": [],
}

latencies = []

print("\n" + "=" * 72)
print("PER-QUERY RESULTS")
print("=" * 72)

for query_id in sorted(records_by_query):

    records = sorted(
        records_by_query[query_id],
        key=lambda x: x["rank"],
    )

    query = records[0]["query"]

    pairs = [[query, record["passage"]] for record in records]

    start = time.perf_counter()

    scores = model.predict(pairs)

    latency = time.perf_counter() - start
    latencies.append(latency)

    scored_records = []

    for record, score in zip(records, scores):
        copied = dict(record)
        copied["reranker_score"] = float(score)
        scored_records.append(copied)

    reranked = sorted(
        scored_records,
        key=lambda x: x["reranker_score"],
        reverse=True,
    )

    relevances = [record["relevance"] for record in reranked]

    p1 = precision_at_k(relevances, 1)
    p3 = precision_at_k(relevances, 3)
    p5 = precision_at_k(relevances, 5)
    rr = reciprocal_rank(relevances)
    ndcg5 = ndcg_at_k(relevances, 5)

    direct_answer_recall = 1.0 if any(rel == 2 for rel in relevances[:5]) else 0.0

    metrics["precision@1"].append(p1)
    metrics["precision@3"].append(p3)
    metrics["precision@5"].append(p5)
    metrics["mrr"].append(rr)
    metrics["ndcg@5"].append(ndcg5)
    metrics["direct_answer_recall@5"].append(direct_answer_recall)

    top = reranked[0]

    print(
        f"{query_id}: "
        f"P@1={p1:.2f} "
        f"P@3={p3:.2f} "
        f"P@5={p5:.2f} "
        f"RR={rr:.2f} "
        f"NDCG@5={ndcg5:.3f} "
        f"Direct@5={int(direct_answer_recall)} "
        f"Latency={latency:.3f}s "
        f"TopRel={top['relevance']} "
        f"BM25Rank={top['rank']}"
    )


print("\n" + "=" * 72)
print("MEAN CROSS-ENCODER METRICS")
print("=" * 72)

for name, values in metrics.items():
    mean_value = sum(values) / len(values)
    print(f"{name}: {mean_value:.4f}")


print("\n" + "=" * 72)
print("LATENCY")
print("=" * 72)

print(f"Average reranking latency: " f"{sum(latencies) / len(latencies):.4f} seconds")

print(f"Minimum reranking latency: " f"{min(latencies):.4f} seconds")

print(f"Maximum reranking latency: " f"{max(latencies):.4f} seconds")
