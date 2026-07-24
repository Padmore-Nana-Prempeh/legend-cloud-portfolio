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

def test_cognito_user_pool_created():
    template = create_template()

    template.resource_count_is("AWS::Cognito::UserPool", 1)

    template.has_resource_properties(
        "AWS::Cognito::UserPool",
        {
            "AutoVerifiedAttributes": ["email"],
            "UsernameAttributes": ["email"],
        },
    )

def test_cognito_user_pool_client_created():
    template = create_template()

    template.resource_count_is("AWS::Cognito::UserPoolClient", 1)

    template.has_resource_properties(
        "AWS::Cognito::UserPoolClient",
        {
            "GenerateSecret": False,
        },
    )

def test_api_gateway_rest_api_created():
    template = create_template()

    template.resource_count_is("AWS::ApiGateway::RestApi", 1)

def test_cognito_api_authorizer_created():
    template = create_template()

    template.resource_count_is("AWS::ApiGateway::Authorizer", 1)

    template.has_resource_properties(
        "AWS::ApiGateway::Authorizer",
        {
            "Type": "COGNITO_USER_POOLS",
        },
    )


def test_auth_test_route_requires_cognito():
    template = create_template()

    template.has_resource_properties(
        "AWS::ApiGateway::Method",
        {
            "HttpMethod": "GET",
            "AuthorizationType": "COGNITO_USER_POOLS",
        },
    )

def test_cloudfront_distribution_created():
    template = create_template()

    template.resource_count_is("AWS::CloudFront::Distribution", 1)

def test_cloudfront_security_headers_policy_created():
    template = create_template()

    template.resource_count_is(
        "AWS::CloudFront::ResponseHeadersPolicy",
        1,
    )

def test_cloudfront_waf_web_acl_created():
    template = create_template()

    template.resource_count_is("AWS::WAFv2::WebACL", 1)

def test_frontend_bucket_deployment_created():
    template = create_template()

    template.resource_count_is(
        "Custom::CDKBucketDeployment",
        1,
    )
