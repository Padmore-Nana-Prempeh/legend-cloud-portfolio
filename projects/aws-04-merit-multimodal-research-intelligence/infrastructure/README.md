# MERIT Infrastructure

This directory contains the AWS CDK application for the MERIT project.

## Purpose

The CDK stack defines the AWS foundation for:

- KMS encryption
- Secure S3 storage
- DynamoDB metadata and idempotency tables
- AWS Systems Manager Parameter Store configuration
- AWS Budgets
- Cost Anomaly Detection subscriptions
- Governance and cost-allocation tags

The primary AWS deployment region is `us-east-1`.

## Local Setup

Move into the infrastructure directory:

```bash
cd infrastructure
```

Create and activate the infrastructure virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install infrastructure dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

This virtual environment is intentionally separate from the root MERIT
virtual environment used for machine learning and application development.

## Validate

Run the infrastructure unit tests:

```bash
python -m pytest tests/unit/test_infrastructure_stack.py -q
```

Synthesize the CloudFormation template:

```bash
cdk synth
```

Review proposed infrastructure changes:

```bash
cdk diff
```

## Deployment Parameters

The stack requires two deployment-time parameters:

- `BudgetAlertEmail`
- `CostAnomalyMonitorArn`

These values are intentionally supplied at deployment time rather than
hard-coded into the repository.

Example:

```bash
cdk deploy \
  --parameters BudgetAlertEmail="<alert-email>" \
  --parameters CostAnomalyMonitorArn="<existing-monitor-arn>"
```

Do not commit personal email addresses, AWS account identifiers, credentials,
or full resource ARNs to the repository.

## Security Controls

The Milestone 2 foundation includes:

- Customer-managed AWS KMS encryption
- KMS key rotation
- S3 Block Public Access
- TLS-only S3 bucket policies
- S3 Bucket Keys
- Versioning for upload and processed-data buckets
- DynamoDB customer-managed KMS encryption
- DynamoDB point-in-time recovery
- Bedrock configuration stored in Systems Manager Parameter Store
- AWS budget notifications
- AWS Cost Anomaly Detection subscription
- Governance and cost-allocation tags

## Current Milestone

This infrastructure implements the MERIT Milestone 2 AWS foundation.

Infrastructure-specific IAM roles and CloudWatch logging resources will be
introduced alongside the application workloads that require them, allowing
permissions and observability settings to remain workload-specific.
