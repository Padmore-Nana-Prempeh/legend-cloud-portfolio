from pathlib import Path
from aws_cdk import (
    CfnParameter,
    Duration,
    Fn,
    RemovalPolicy,
    Stack,
    Tags,
    aws_iam as iam,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_kms as kms,
    aws_s3 as s3,
    aws_ce as ce,
    aws_ssm as ssm,
    aws_s3_deployment as s3deploy,
    aws_cognito as cognito,
    aws_budgets as budgets,
    aws_wafv2 as wafv2,
)
from constructs import Construct


class InfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    # Deployment-time alert email; kept out of public source code
        alert_email = CfnParameter(
            self,
           "BudgetAlertEmail",
           type="String",
           description="Email address for MERIT budget and cost anomaly alerts",
           no_echo=True,
        )

        # Existing account-level AWS Services anomaly monitor ARN
        anomaly_monitor_arn = CfnParameter(
           self,
           "CostAnomalyMonitorArn",
           type="String",
           description="ARN of the existing AWS Services Cost Anomaly Detection monitor",
           no_echo=True,
        )
        # Existing MERIT CloudFront distribution ARN used to scope KMS access
        cloudfront_distribution_arn = CfnParameter(
            self,
            "CloudFrontDistributionArn",
            type="String",
            description="ARN of the deployed MERIT CloudFront distribution",
            no_echo=True,
        )
        # Browser origin allowed to call the MERIT API
        frontend_allowed_origin = CfnParameter(
            self,
            "FrontendAllowedOrigin",
            type="String",
            description="Allowed browser origin for MERIT API CORS",
            no_echo=True,
        )



    # Common governance and cost-allocation tags
        Tags.of(self).add("Project", "MERIT")
        Tags.of(self).add("Environment", "dev")
        Tags.of(self).add("Owner", "Legend-PNP")
        Tags.of(self).add("ManagedBy", "CDK")
        Tags.of(self).add("CostCenter", "Portfolio")
        Tags.of(self).add("DataClassification", "Internal")

        # Cognito user pool for MERIT authentication
        self.user_pool = cognito.UserPool(
            self,
            "MeritUserPool",
            user_pool_name="merit-dev-users",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            removal_policy=RemovalPolicy.DESTROY,
        )
        # Cognito app client for the MERIT frontend
        self.user_pool_client = self.user_pool.add_client(
            "MeritUserPoolClient",
            user_pool_client_name="merit-dev-web-client",
            generate_secret=False,
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True,
            ),
        )

        # REST API entry point for MERIT backend services
        self.api = apigateway.RestApi(
            self,
            "MeritRestApi",
            rest_api_name="merit-dev-api",
            description="REST API for the MERIT research intelligence platform",
            deploy_options=apigateway.StageOptions(
                stage_name="dev",
            ),
        )
                # Cognito authorizer for protected MERIT API routes
        self.cognito_authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self,
            "MeritCognitoAuthorizer",
            cognito_user_pools=[self.user_pool],
            authorizer_name="merit-dev-cognito-authorizer",
        )

        # Protected test endpoint used to verify JWT authorization in M3
        auth_test = self.api.root.add_resource("auth-test")

        # Browser CORS preflight for the local MERIT frontend
        auth_test.add_cors_preflight(
            allow_origins=[frontend_allowed_origin.value_as_string],
            allow_methods=["GET"],
            allow_headers=[
                "Authorization",
                "Content-Type",
            ],
        )

        auth_test.add_method(
            "GET",
            apigateway.MockIntegration(
                integration_responses=[
                    apigateway.IntegrationResponse(
                        status_code="200",
                        response_parameters={
                            "method.response.header.Access-Control-Allow-Origin": Fn.join(
                                "",
                                [
                                    "'",
                                    frontend_allowed_origin.value_as_string,
                                    "'",

                                ],

                            ),
                        },
                    )
                ],
                request_templates={
                    "application/json": '{"statusCode": 200}'
                },
            ),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=self.cognito_authorizer,
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": True,
                    },
                )
            ],
        )

        # MERIT foundation KMS key
        self.merit_key = kms.Key(
            self,
            "MeritKey",
            alias="alias/merit-dev",
            description="KMS key for MERIT development resources",
            enable_key_rotation=True,
            removal_policy=RemovalPolicy.DESTROY,
            pending_window=Duration.days(7),
        )
        # Secure bucket for original user uploads
        self.upload_bucket = s3.Bucket(
            self,
            "MeritUploadBucket",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=self.merit_key,
            bucket_key_enabled=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
    # Secure bucket for processed and derived document artifacts
        self.processed_bucket = s3.Bucket(
            self,
            "MeritProcessedBucket",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=self.merit_key,
            bucket_key_enabled=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
    # Private bucket for the static frontend
        self.frontend_bucket = s3.Bucket(
            self,
            "MeritFrontendBucket",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=self.merit_key,
            bucket_key_enabled=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
                # Private S3 origin accessed only through CloudFront OAC
        frontend_origin = origins.S3BucketOrigin.with_origin_access_control(
            self.frontend_bucket,
        )
                # Security headers applied to MERIT frontend responses
        self.security_headers_policy = cloudfront.ResponseHeadersPolicy(
            self,
            "MeritSecurityHeadersPolicy",
            response_headers_policy_name="merit-dev-security-headers",
            remove_headers=[
                "x-amz-server-side-encryption",
                "x-amz-server-side-encryption-aws-kms-key-id",
                "x-amz-server-side-encryption-bucket-key-enabled",
            ],
            security_headers_behavior=cloudfront.ResponseSecurityHeadersBehavior(
                content_type_options=cloudfront.ResponseHeadersContentTypeOptions(
                    override=True,
                ),
                frame_options=cloudfront.ResponseHeadersFrameOptions(
                    frame_option=cloudfront.HeadersFrameOption.DENY,
                    override=True,
                ),
                referrer_policy=cloudfront.ResponseHeadersReferrerPolicy(
                    referrer_policy=cloudfront.HeadersReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN,
                    override=True,
                ),
                strict_transport_security=cloudfront.ResponseHeadersStrictTransportSecurity(
                    access_control_max_age=Duration.days(365),
                    include_subdomains=True,
                    preload=True,
                    override=True,
                ),
            ),
        )
                # AWS WAF protection for the MERIT CloudFront distribution
        self.web_acl = wafv2.CfnWebACL(
            self,
            "MeritWebAcl",
            name="merit-dev-web-acl",
            scope="CLOUDFRONT",
            default_action=wafv2.CfnWebACL.DefaultActionProperty(
                allow={},
            ),
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name="merit-dev-web-acl",
                sampled_requests_enabled=True,
            ),
            rules=[
                wafv2.CfnWebACL.RuleProperty(
                    name="AWSManagedRulesCommonRuleSet",
                    priority=0,
                    override_action=wafv2.CfnWebACL.OverrideActionProperty(
                        none={},
                    ),
                    statement=wafv2.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                            vendor_name="AWS",
                            name="AWSManagedRulesCommonRuleSet",
                        )
                    ),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="merit-common-rules",
                        sampled_requests_enabled=True,
                    ),
                ),
                wafv2.CfnWebACL.RuleProperty(
                    name="AWSManagedRulesKnownBadInputsRuleSet",
                    priority=1,
                    override_action=wafv2.CfnWebACL.OverrideActionProperty(
                        none={},
                    ),
                    statement=wafv2.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                            vendor_name="AWS",
                            name="AWSManagedRulesKnownBadInputsRuleSet",
                        )
                    ),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="merit-known-bad-inputs",
                        sampled_requests_enabled=True,
                    ),
                ),
                wafv2.CfnWebACL.RuleProperty(
                    name="RateLimitPerIp",
                    priority=2,
                    action=wafv2.CfnWebACL.RuleActionProperty(
                        block={},
                    ),
                    statement=wafv2.CfnWebACL.StatementProperty(
                        rate_based_statement=wafv2.CfnWebACL.RateBasedStatementProperty(
                            aggregate_key_type="IP",
                            limit=2000,
                        )
                    ),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="merit-rate-limit",
                        sampled_requests_enabled=True,
                    ),
                ),
            ],
        )
                # Rewrite clean Next.js static-export routes to their index.html objects.
        self.frontend_route_rewrite = cloudfront.Function(
            self,
            "MeritFrontendRouteRewrite",
            code=cloudfront.FunctionCode.from_inline(
                """
function handler(event) {
    var request = event.request;
    var uri = request.uri;

    if (uri.endsWith("/")) {
        request.uri += "index.html";
    } else if (!uri.includes(".")) {
        request.uri += "/index.html";
    }

    return request;
}
"""
            ),
            runtime=cloudfront.FunctionRuntime.JS_2_0,
        )





        # CloudFront distribution for the MERIT frontend
        self.frontend_distribution = cloudfront.Distribution(
            self,
            "MeritFrontendDistribution",
            default_root_object="index.html",
            web_acl_id=self.web_acl.attr_arn,
            default_behavior=cloudfront.BehaviorOptions(
                origin=frontend_origin,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                response_headers_policy=self.security_headers_policy,
                function_associations=[
                    cloudfront.FunctionAssociation(
                        function=self.frontend_route_rewrite,
                        event_type=cloudfront.FunctionEventType.VIEWER_REQUEST,
                    )
                ],
            ),
        )

        frontend_build_path = (
            Path(__file__).resolve().parents[2] / "frontend" / "out"
        )

        # Deploy the statically exported Next.js frontend to the private S3 bucket
        self.frontend_deployment = s3deploy.BucketDeployment(
            self,
            "MeritFrontendDeployment",
            sources=[
                s3deploy.Source.asset(str(frontend_build_path)),
            ],
            destination_bucket=self.frontend_bucket,
            distribution=self.frontend_distribution,
            distribution_paths=["/*"],
        )
        # Scope CloudFront KMS decrypt permission to this deployed distribution only.
        # This replaces the initial CDK distribution/* wildcard used to avoid
        # a circular dependency during the first OAC deployment.
        scoped_key_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": f"arn:aws:iam::{self.account}:root",
                    },
                    "Action": "kms:*",
                    "Resource": "*",
                },
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "cloudfront.amazonaws.com",
                    },
                    "Action": "kms:Decrypt",
                    "Resource": "*",
                    "Condition": {
                        "StringEquals": {
                            "AWS:SourceArn": cloudfront_distribution_arn.value_as_string,
                        }
                    },
                },
            ],
        }

        cfn_merit_key = self.merit_key.node.default_child
        cfn_merit_key.key_policy = scoped_key_policy





       # Email subscription for MERIT cost anomalies
        self.cost_anomaly_subscription = ce.CfnAnomalySubscription(
            self,
            "MeritCostAnomalySubscription",
            frequency="DAILY",
            monitor_arn_list=[
            anomaly_monitor_arn.value_as_string,
        ],
            subscribers=[
                ce.CfnAnomalySubscription.SubscriberProperty(
                    address=alert_email.value_as_string,
                    type="EMAIL",
                )
            ],
            subscription_name="MERIT-cost-anomaly-alerts",
            threshold=5,
        )

    # DynamoDB table for document metadata and processing state
        self.metadata_table = dynamodb.Table(
            self,
            "MeritMetadataTable",
            partition_key=dynamodb.Attribute(
                name="PK",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="SK",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            encryption=dynamodb.TableEncryption.CUSTOMER_MANAGED,
            encryption_key=self.merit_key,
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
            point_in_time_recovery_enabled=True,
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )
    # DynamoDB table for idempotent ingestion processing
        self.idempotency_table = dynamodb.Table(
            self,
            "MeritIdempotencyTable",
            partition_key=dynamodb.Attribute(
                name="documentHash",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            encryption=dynamodb.TableEncryption.CUSTOMER_MANAGED,
            encryption_key=self.merit_key,
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled=True,
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )
    # Bedrock model configuration stored in SSM Parameter Store
        self.embedding_model_parameter = ssm.StringParameter(
            self,
            "MeritEmbeddingModelParameter",
            parameter_name="/merit/dev/bedrock/embedding-model-id",
            string_value="amazon.titan-embed-text-v2:0",
            description="Pinned embedding model ID for MERIT",
        )

        self.generation_model_parameter = ssm.StringParameter(
            self,
            "MeritGenerationModelParameter",
            parameter_name="/merit/dev/bedrock/generation-inference-profile-id",
            string_value="us.amazon.nova-2-lite-v1:0",
            description="Pinned Bedrock generation inference profile for MERIT",
        )

        self.embedding_dimension_parameter = ssm.StringParameter(
            self,
            "MeritEmbeddingDimensionParameter",
            parameter_name="/merit/dev/bedrock/embedding-dimension",
            string_value="512",
            description="Embedding vector dimension used by MERIT",
        )
    # Monthly AWS cost budget for the MERIT development environment
        self.merit_budget = budgets.CfnBudget(
            self,
            "MeritMonthlyBudget",
            budget=budgets.CfnBudget.BudgetDataProperty(
                budget_name="MERIT-dev-monthly-budget",
                budget_type="COST",
                time_unit="MONTHLY",
                budget_limit=budgets.CfnBudget.SpendProperty(
                    amount=25,
                    unit="USD",
                ),
            ),
            notifications_with_subscribers=[
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        comparison_operator="GREATER_THAN",
                        notification_type="ACTUAL",
                        threshold=50,
                        threshold_type="PERCENTAGE",
                    ),
                    subscribers=[
                        budgets.CfnBudget.SubscriberProperty(
                            address=alert_email.value_as_string,
                            subscription_type="EMAIL",
                        )
                    ],
                ),
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        comparison_operator="GREATER_THAN",
                        notification_type="ACTUAL",
                        threshold=80,
                        threshold_type="PERCENTAGE",
                    ),
                    subscribers=[
                        budgets.CfnBudget.SubscriberProperty(
                            address=alert_email.value_as_string,
                            subscription_type="EMAIL",
                        )
                    ],
                ),
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        comparison_operator="GREATER_THAN",
                        notification_type="ACTUAL",
                        threshold=100,
                        threshold_type="PERCENTAGE",
                    ),
                    subscribers=[
                        budgets.CfnBudget.SubscriberProperty(
                            address=alert_email.value_as_string,
                            subscription_type="EMAIL",
                        )
                    ],
                ),
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        comparison_operator="GREATER_THAN",
                        notification_type="FORECASTED",
                        threshold=100,
                        threshold_type="PERCENTAGE",
                    ),
                    subscribers=[
                        budgets.CfnBudget.SubscriberProperty(
                            address=alert_email.value_as_string,
                            subscription_type="EMAIL",
                        )
                    ],
                ),
            ],
        )
