# MERIT Architecture

## Multimodal Evidence Retrieval and Research Intelligence Toolkit

MERIT is a secure, event-driven AWS research intelligence platform.

The architecture combines four AWS Solutions Architect learning domains:

1. Automation and Governance
2. DNS and Network Routing
3. Application Integration
4. Artificial Intelligence and Machine Learning

The platform is designed to:

- securely ingest research documents, images, and recorded presentations;
- process content asynchronously;
- extract structured information;
- generate embeddings;
- perform hybrid evidence retrieval;
- rerank evidence using a custom PyTorch model;
- generate grounded answers with citations;
- enforce authentication and tenant isolation;
- provide observability, governance, failure handling, and cost controls.

The architecture diagram in this directory is the project's primary implementation blueprint.

## Core query path

User Question

→ API Gateway

→ Query Handler

→ Query Embedding

→ Hybrid Retrieval

→ Custom PyTorch Evidence Reranker

→ Amazon Bedrock + Guardrails

→ Grounded Answer with Citations

## Core ingestion path

Secure Upload

→ Amazon S3

→ EventBridge

→ Amazon SQS

→ Idempotency Consumer

→ AWS Step Functions

→ AI/ML Extraction

→ Chunking and Embedding

→ Persistent Storage

→ Notification
