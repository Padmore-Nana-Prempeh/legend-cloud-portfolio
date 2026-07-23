import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.infrastructure_stack import InfrastructureStack


def create_template() -> assertions.Template:
    app = core.App()
    stack = InfrastructureStack(app, "TestInfrastructureStack")
    return assertions.Template.from_stack(stack)


def test_kms_key_rotation_enabled():
    template = create_template()

    template.has_resource_properties(
        "AWS::KMS::Key",
        {
            "EnableKeyRotation": True,
            "PendingWindowInDays": 7,
        },
    )


def test_three_s3_buckets_created():
    template = create_template()

    template.resource_count_is("AWS::S3::Bucket", 3)


def test_s3_buckets_block_public_access():
    template = create_template()

    template.has_resource_properties(
        "AWS::S3::Bucket",
        {
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": True,
                "BlockPublicPolicy": True,
                "IgnorePublicAcls": True,
                "RestrictPublicBuckets": True,
            }
        },
    )


def test_s3_buckets_use_kms_encryption():
    template = create_template()

    template.has_resource_properties(
        "AWS::S3::Bucket",
        {
            "BucketEncryption": {
                "ServerSideEncryptionConfiguration": [
                    {
                        "BucketKeyEnabled": True,
                        "ServerSideEncryptionByDefault": {
                            "SSEAlgorithm": "aws:kms",
                        },
                    }
                ]
            }
        },
    )


def test_metadata_table_configuration():
    template = create_template()

    template.has_resource_properties(
        "AWS::DynamoDB::Table",
        {
            "BillingMode": "PAY_PER_REQUEST",
            "KeySchema": [
                {
                    "AttributeName": "PK",
                    "KeyType": "HASH",
                },
                {
                    "AttributeName": "SK",
                    "KeyType": "RANGE",
                },
            ],
            "PointInTimeRecoverySpecification": {
                "PointInTimeRecoveryEnabled": True,
            },
        },
    )


def test_idempotency_table_configuration():
    template = create_template()

    template.has_resource_properties(
        "AWS::DynamoDB::Table",
        {
            "BillingMode": "PAY_PER_REQUEST",
            "KeySchema": [
                {
                    "AttributeName": "documentHash",
                    "KeyType": "HASH",
                }
            ],
            "PointInTimeRecoverySpecification": {
                "PointInTimeRecoveryEnabled": True,
            },
        },
    )


def test_bedrock_ssm_parameters_created():
    template = create_template()

    template.has_resource_properties(
        "AWS::SSM::Parameter",
        {
            "Name": "/merit/dev/bedrock/embedding-model-id",
            "Value": "amazon.titan-embed-text-v2:0",
        },
    )

    template.has_resource_properties(
        "AWS::SSM::Parameter",
        {
            "Name": "/merit/dev/bedrock/generation-inference-profile-id",
            "Value": "us.amazon.nova-2-lite-v1:0",
        },
    )

    template.has_resource_properties(
        "AWS::SSM::Parameter",
        {
            "Name": "/merit/dev/bedrock/embedding-dimension",
            "Value": "512",
        },
    )


def test_monthly_budget_created():
    template = create_template()

    template.has_resource_properties(
        "AWS::Budgets::Budget",
        {
            "Budget": {
                "BudgetLimit": {
                    "Amount": 25,
                    "Unit": "USD",
                },
                "BudgetName": "MERIT-dev-monthly-budget",
                "BudgetType": "COST",
                "TimeUnit": "MONTHLY",
            }
        },
    )


def test_cost_anomaly_subscription_created():
    template = create_template()

    template.has_resource_properties(
        "AWS::CE::AnomalySubscription",
        {
            "Frequency": "DAILY",
            "SubscriptionName": "MERIT-cost-anomaly-alerts",
            "Threshold": 5,
        },
    )
