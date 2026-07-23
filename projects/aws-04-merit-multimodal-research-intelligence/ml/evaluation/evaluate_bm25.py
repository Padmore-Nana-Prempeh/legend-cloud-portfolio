import json
import math
from collections import defaultdict
from pathlib import Path

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


metrics = {
    "precision@1": [],
    "precision@3": [],
    "precision@5": [],
    "mrr": [],
    "ndcg@5": [],
    "direct_answer_recall@5": [],
}


print("=" * 72)
print("MERIT BM25 FEASIBILITY EVALUATION")
print("=" * 72)

for query_id in sorted(records_by_query):
    records = sorted(
        records_by_query[query_id],
        key=lambda x: x["rank"],
    )

    relevances = [record["relevance"] for record in records]

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

    print(
        f"{query_id}: "
        f"P@1={p1:.2f} "
        f"P@3={p3:.2f} "
        f"P@5={p5:.2f} "
        f"RR={rr:.2f} "
        f"NDCG@5={ndcg5:.3f} "
        f"Direct@5={int(direct_answer_recall)}"
    )


print("\n" + "=" * 72)
print("MEAN METRICS")
print("=" * 72)

for name, values in metrics.items():
    mean_value = sum(values) / len(values)
    print(f"{name}: {mean_value:.4f}")
