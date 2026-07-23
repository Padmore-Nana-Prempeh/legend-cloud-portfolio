from pathlib import Path

from ml.evaluation.load_annotations import load_annotations


def test_sample_annotations_load() -> None:
    path = Path("ml/data/sample/relevance_annotations.jsonl")

    records = load_annotations(path)

    assert len(records) == 4
    assert all(record["relevance"] in {0, 1, 2} for record in records)
