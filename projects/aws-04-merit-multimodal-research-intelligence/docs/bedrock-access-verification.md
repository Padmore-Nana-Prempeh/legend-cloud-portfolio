# Amazon Bedrock Access Verification

## Region

Primary AWS Region:

`us-east-1`

## AWS CLI Identity Verification

Command used:

```bash
aws sts get-caller-identity
```

Result:

- AWS CLI authentication succeeded.
- The development IAM identity was recognized successfully.
- No account ID or full IAM ARN is recorded in this public documentation.

## Generation Model Verification

Foundation model:

`amazon.nova-2-lite-v1:0`

Inference profile:

`us.amazon.nova-2-lite-v1:0`

Verification results:

- Model status: `ACTIVE`
- Inference profile status: `ACTIVE`
- Inference profile type: `SYSTEM_DEFINED`
- Invocation succeeded through Amazon Bedrock Runtime
- Test response matched the requested output exactly
- Observed test latency: `607 ms`

The successful invocation confirmed that the MERIT development identity can perform Bedrock generation requests using Nova 2 Lite.

## Embedding Model Verification

Embedding model:

`amazon.titan-embed-text-v2:0`

Verification results:

- Model status: `ACTIVE`
- Inference type: `ON_DEMAND`
- Input modality: `TEXT`
- Output modality: `EMBEDDING`
- Test invocation succeeded
- Configured embedding dimensions: `512`
- Normalization enabled: `true`
- Returned embedding dimensions: `512`
- Test input token count: `10`

The returned vector confirmed that Titan Text Embeddings V2 can be invoked successfully from the MERIT development environment.

## Initial MERIT Model Decision

MERIT will initially use:

- **Amazon Titan Text Embeddings V2** for query and document embeddings.
- **Amazon Nova 2 Lite** through the US inference profile for grounded answer generation.

Current identifiers:

```text
Embedding model:
amazon.titan-embed-text-v2:0

Generation inference profile:
us.amazon.nova-2-lite-v1:0

Embedding dimensions:
512

Primary region:
us-east-1
```

These identifiers are stored in AWS Systems Manager Parameter Store and are not hard-coded into application code.

## Verification Status

| Check | Status |
|---|---|
| AWS CLI identity | Passed |
| Bedrock control plane access | Passed |
| Nova 2 Lite availability | Passed |
| Nova 2 Lite inference profile | Passed |
| Nova 2 Lite runtime invocation | Passed |
| Titan Text Embeddings V2 availability | Passed |
| Titan embedding runtime invocation | Passed |
| 512-dimensional embedding validation | Passed |

This verification was completed before building the AWS infrastructure foundation so that later MERIT milestones do not depend on unverified model availability.


