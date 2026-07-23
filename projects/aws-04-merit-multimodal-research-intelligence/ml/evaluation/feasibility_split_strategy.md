# MERIT Milestone 1B — Split and Leakage Strategy

## Purpose

The Milestone 1B dataset is a small feasibility dataset used to validate:

- annotation schema
- chunk identifiers
- retrieval metrics
- pretrained cross-encoder reranking
- latency behavior
- end-to-end ML plumbing

It is not intended to produce final published model-performance claims.

## Current feasibility corpus

- Documents: 4
- Evaluation queries: 20
- Query-passage annotations: 100
- Relevance scale:
  - 0 = not relevant
  - 1 = partially relevant
  - 2 = highly relevant

## Leakage risk

The current candidate pool contains passages from a very small number of documents.

Randomly splitting individual query-passage rows into training, validation, and test sets would create leakage because chunks from the same source document could appear in multiple splits.

This would produce overly optimistic estimates of reranker performance.

## Milestone 1B decision

No custom reranker is trained on the 100 feasibility annotations.

Instead, the project evaluates the pretrained cross-encoder:

`cross-encoder/ms-marco-MiniLM-L-6-v2`

in zero-shot reranking mode.

The same human labels are used only as an evaluation reference for comparing:

1. BM25 ordering
2. pretrained cross-encoder ordering

No model parameters are updated using these labels.

## Full-dataset strategy

During the later full ML dataset milestone:

- approximately 30–60 reusable research documents will be collected
- approximately 100–200 questions will be created
- query-passage relevance will use the same 0/1/2 scale
- splitting will occur at the document level rather than the chunk level

The intended split is approximately:

- 70% training documents
- 15% validation documents
- 15% test documents

All chunks derived from the same document must remain in the same split.

## Acceptance rule

A performance result will only be described as a trained-model evaluation when:

- the model was trained only on training documents
- hyperparameters were selected using validation documents
- final metrics were calculated once on unseen test documents
- no document appears in more than one split
