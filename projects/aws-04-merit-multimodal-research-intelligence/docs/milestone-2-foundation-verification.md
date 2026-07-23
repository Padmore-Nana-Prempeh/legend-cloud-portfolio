# MERIT Milestone 2 — AWS Foundation Verification

## Milestone

**M2 — AWS Infrastructure Foundation**

MERIT's foundational AWS resources were provisioned using AWS CDK and successfully deployed in the `us-east-1` Region.

This milestone establishes the secure storage, encryption, metadata, configuration, governance, and cost-control foundation required by later MERIT workloads.

---

## Deployment Status

AWS CloudFormation deployment status:

`CREATE_COMPLETE`

The infrastructure stack was successfully synthesized and deployed using AWS CDK.

Infrastructure unit tests also completed successfully:

```text
9 passed
```

---

## AWS KMS

A customer-managed AWS KMS key was created for MERIT development resources.

Verified controls:

- Key rotation enabled
- 365-day rotation period
- Development alias configured
- Explicit development removal policy
- Seven-day pending deletion window
- MERIT governance and cost-allocation tags applied

The key is used by the MERIT S3 buckets and DynamoDB tables.

---

## Amazon S3

Three S3 buckets were provisioned for distinct MERIT responsibilities:

1. Upload storage
2. Processed-content storage
3. Frontend storage

Verified security controls:

- S3 Block Public Access enabled
- Customer-managed KMS encryption enabled
- S3 Bucket Keys enabled
- TLS-only access enforced through bucket policies
- Upload bucket versioning enabled
- Processed-content bucket versioning enabled
- Frontend bucket intentionally does not require versioning at this stage
- Development removal policies configured

The frontend bucket remains private. CloudFront access controls will be introduced during the edge/authentication milestone.

---

## Amazon DynamoDB

Two DynamoDB tables were provisioned.

### Metadata Table

Purpose:

Store document and application metadata required by later MERIT ingestion and retrieval workflows.

Verified configuration:

- Composite primary key using `PK` and `SK`
- On-demand billing
- Customer-managed KMS encryption
- Point-in-time recovery enabled
- MERIT governance tags applied

### Idempotency Table

Purpose:

Support duplicate-ingestion protection and idempotent event-driven processing.

Verified configuration:

- Partition key: `documentHash`
- On-demand billing
- Customer-managed KMS encryption
- Point-in-time recovery enabled
- MERIT governance tags applied

---

## AWS Systems Manager Parameter Store

The following MERIT configuration values are stored in Parameter Store rather than hard-coded into application code:

- Bedrock embedding model identifier
- Bedrock generation inference profile identifier
- Embedding vector dimension

Verified values correspond to the models tested during the Bedrock access-verification step.

This creates a configuration boundary that will allow future application components to retrieve model settings without embedding deployment-specific values directly in source code.

---

## Amazon Bedrock Configuration

The foundation is configured for:

### Embeddings

Amazon Titan Text Embeddings V2

Embedding dimension:

`512`

### Generation

Amazon Nova 2 Lite through a system-defined inference profile.

Both embedding and generation access were tested successfully before the infrastructure deployment.

Detailed verification is recorded in:

`docs/bedrock-access-verification.md`

---

## AWS Budgets

A monthly development budget was provisioned for MERIT.

Budget amount:

`$25 USD`

Configured notifications:

- 50% actual spend
- 80% actual spend
- 100% actual spend
- 100% forecasted spend

The alert email address is provided only as a deployment-time CloudFormation parameter and is not stored in the public source repository.

---

## AWS Cost Anomaly Detection

MERIT uses the existing account-level AWS Services anomaly monitor instead of attempting to create a duplicate dimensional service monitor.

A MERIT-specific anomaly subscription was created with:

- Daily notification frequency
- Email delivery
- `$5` anomaly threshold

This design was selected after CloudFormation identified that an AWS Services dimensional monitor already existed in the account.

The monitor ARN is supplied as a deployment-time parameter and is not hard-coded in source control.

---

## Governance Tags

The following project tags are applied to supported MERIT resources:

```text
Project=MERIT
Environment=dev
Owner=Legend-PNP
ManagedBy=CDK
CostCenter=Portfolio
DataClassification=Internal
```

These tags provide a consistent basis for:

- Cost allocation
- Resource identification
- Environment separation
- Governance
- Future automation

---

## Infrastructure Testing

The CDK infrastructure includes automated unit tests covering:

- KMS key rotation
- S3 bucket creation
- S3 public-access protection
- S3 KMS encryption
- DynamoDB metadata-table configuration
- DynamoDB idempotency-table configuration
- Bedrock Parameter Store configuration
- Monthly budget creation
- Cost Anomaly Detection subscription

Latest result:

```text
9 passed
```

---

## Security and Privacy Review

Before committing the infrastructure to GitHub:

- AWS access-key patterns were scanned
- Temporary credential patterns were scanned
- Full AWS ARN patterns were scanned
- AWS account-ID patterns were scanned
- Personal deployment email addresses were excluded
- `.venv` directories were excluded
- `cdk.out` was excluded
- Python cache files were excluded

No AWS credentials, AWS account IDs, or deployment-specific ARNs were committed to the public repository.

---

## Deployment Lessons

Two deployment issues were encountered and resolved during M2.

### Existing Cost Anomaly Monitor

AWS already had an account-level dimensional AWS Services anomaly monitor.

Rather than creating a duplicate monitor, MERIT reuses the existing monitor and creates only its own anomaly subscription.

### Cost Anomaly Email Frequency

An immediate Cost Anomaly Detection subscription could not use direct email delivery.

The MERIT subscription was therefore configured to use:

`DAILY`

frequency with email notifications.

These troubleshooting decisions are intentionally reflected in the final infrastructure code rather than hidden from the project history.

---

## Deferred Infrastructure

Some resources are intentionally deferred until the application workloads that require them are introduced.

These include:

- Application-specific IAM roles
- Lambda log groups and retention policies
- API Gateway logging
- CloudFront edge configuration
- Cognito authentication
- Service-specific observability resources

This avoids creating unused placeholder resources and allows least-privilege IAM permissions and logging policies to be designed around real workloads.

---

## Milestone 2 Acceptance Summary

Milestone 2 is considered complete because MERIT now has:

- AWS CDK infrastructure
- Customer-managed encryption
- Secure S3 storage
- DynamoDB metadata storage
- DynamoDB idempotency support
- Parameter Store configuration
- Verified Bedrock model configuration
- Budget controls
- Cost anomaly monitoring
- Governance tagging
- Automated infrastructure tests
- Successful CloudFormation deployment
- Public-source privacy review

**Milestone 2 Status: COMPLETE**

The next implementation milestone is:

**M3 — Authentication and Edge**
