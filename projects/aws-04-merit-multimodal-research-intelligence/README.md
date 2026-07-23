# MERIT

## Multimodal Evidence Retrieval and Research Intelligence Toolkit

MERIT is a multimodal research-intelligence platform designed and built on AWS.

The system securely ingests research documents, scanned files, images, and recorded presentations; processes them through an event-driven architecture; extracts and indexes evidence; reranks candidate passages using a custom PyTorch machine-learning model; and generates grounded answers with verifiable citations using Amazon Bedrock.

---

## Project Status

🚧 Active Development

Current stage:

**Milestone 1 — Repository Foundation**

Next:

**Milestone 1B — Local ML Feasibility Spike**

---

## Core Architecture

MERIT combines:

- AWS Route 53
- AWS WAF
- Amazon CloudFront
- Amazon Cognito
- Amazon API Gateway
- AWS Lambda
- Amazon S3
- Amazon EventBridge
- Amazon SQS
- AWS Step Functions
- Amazon Textract
- Amazon Transcribe
- Amazon Rekognition
- Amazon Comprehend
- Amazon Bedrock
- Amazon OpenSearch
- Amazon DynamoDB
- Amazon SNS
- AWS IAM
- AWS KMS
- Amazon CloudWatch
- AWS CloudTrail
- AWS Config

Infrastructure will be managed using AWS CDK and CloudFormation.

---

## Core Machine Learning Contribution

The main custom ML component is an evidence reranking model implemented with PyTorch.

The retrieval architecture is:

Question

→ Hybrid Retrieval

→ Custom PyTorch Reranker

→ Highest-Ranked Evidence

→ Grounded Generation

→ Citation Validation

The custom reranker will be evaluated against:

1. TF-IDF
2. BM25
3. Embedding similarity
4. Hybrid retrieval
5. Hybrid retrieval + custom reranking

Metrics will include:

- Precision@K
- Recall@K
- Mean Reciprocal Rank
- NDCG@K
- Mean Average Precision
- Retrieval latency
- Reranking latency
- End-to-end latency

No numerical performance result will be published unless it is reproduced from the project's evaluation code.

---

## Development Strategy

MERIT is being developed incrementally through vertical slices.

The first working MVP will support:

Authenticated User

→ Secure PDF Upload

→ Event-Driven Processing

→ Textract Extraction

→ Persistent Results

→ Processing Status

→ Notification

Retrieval, reranking, RAG, and multimodal capabilities will then be added incrementally.

---

## Security Principles

MERIT is designed around:

- least-privilege IAM;
- encryption at rest and in transit;
- private object storage;
- tenant-scoped retrieval;
- JWT-based authentication;
- idempotent processing;
- dead-letter queues;
- prompt-injection awareness;
- citation validation;
- secure deletion;
- centralized monitoring and audit logging.

---

## Repository Structure

```text
architecture/     Architecture diagrams and design documentation
backend/          Python backend services and Lambda functions
infrastructure/   AWS CDK infrastructure
frontend/         Web interface
ml/               ML baselines, reranker, evaluation and experiments
tests/            Unit and integration tests
docs/             Technical documentation
scripts/          Development and deployment utilities
demo/             Safe demonstration assets
