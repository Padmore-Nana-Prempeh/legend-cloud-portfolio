from aws_cdk import (
    CfnParameter,
    Duration,
    RemovalPolicy,
    Stack,
    Tags,
    aws_dynamodb as dynamodb,
    aws_kms as kms,
    aws_s3 as s3,
    aws_ce as ce,
    aws_ssm as ssm,
    aws_budgets as budgets,
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
            
	
	# Common governance and cost-allocation tags
        Tags.of(self).add("Project", "MERIT")
        Tags.of(self).add("Environment", "dev")
        Tags.of(self).add("Owner", "Legend-PNP")
        Tags.of(self).add("ManagedBy", "CDK")
        Tags.of(self).add("CostCenter", "Portfolio")
        Tags.of(self).add("DataClassification", "Internal")

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
