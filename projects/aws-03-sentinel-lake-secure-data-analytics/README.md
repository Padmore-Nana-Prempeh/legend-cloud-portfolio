# SentinelLake: End-to-End Healthcare Data Analytics & Monitoring Pipeline on AWS

![AWS](https://img.shields.io/badge/AWS-Cloud-orange)
![Amazon S3](https://img.shields.io/badge/Amazon%20S3-Storage-green)
![AWS Glue](https://img.shields.io/badge/AWS%20Glue-Data%20Catalog-blue)
![Amazon Athena](https://img.shields.io/badge/Amazon%20Athena-SQL-purple)
![Amazon CloudWatch](https://img.shields.io/badge/Amazon%20CloudWatch-Monitoring-red)
![AWS CloudTrail](https://img.shields.io/badge/AWS%20CloudTrail-Auditing-yellow)
![Amazon EventBridge](https://img.shields.io/badge/Amazon%20EventBridge-Automation-blue)
![Amazon SNS](https://img.shields.io/badge/Amazon%20SNS-Notifications-orange)
![License](https://img.shields.io/badge/License-MIT-success)

An end-to-end AWS cloud data engineering project that demonstrates secure healthcare data ingestion, automated metadata discovery, serverless SQL analytics, operational monitoring, audit logging, event-driven automation, and real-time security notifications.

---

#  Project Overview

SentinelLake is a cloud-native healthcare analytics platform built entirely with managed AWS services. The project demonstrates how healthcare data can be securely ingested, cataloged, transformed, queried, monitored, audited, and protected using an event-driven architecture.

Patient records are uploaded into Amazon S3, automatically cataloged by AWS Glue, transformed into curated datasets with Amazon Athena, and queried through SQL views for analytical reporting. Beyond analytics, the project incorporates operational monitoring with Amazon CloudWatch, governance through AWS CloudTrail, automated event detection using Amazon EventBridge, and real-time email notifications delivered by Amazon SNS.

Rather than focusing solely on analytics, SentinelLake illustrates how modern cloud data platforms integrate security, observability, automation, and governance into a complete production-style solution.

---

#  Business Problem

Healthcare organizations generate large volumes of structured patient data that must be stored securely, queried efficiently, and continuously monitored. Traditional on-premises data warehouses often require significant infrastructure management while providing limited automation for monitoring and auditing.

The objective of this project was to design a serverless AWS solution capable of:

- securely storing healthcare datasets
- automatically discovering newly uploaded data
- enabling SQL analytics without managing database servers
- creating curated analytical datasets
- providing operational visibility through monitoring dashboards
- recording all AWS management activities for governance
- detecting critical administrative events automatically
- notifying administrators immediately when important security events occur

The final solution demonstrates how managed AWS services can be combined into a scalable, secure, and event-driven analytics platform.

---

#  Solution Architecture

The architecture below illustrates the complete SentinelLake workflow from data ingestion through analytics, monitoring, governance, automation, and notification.

<p align="center">
<img src="screenshots/38-sentinellake-solution-architecture.png" width="100%">
</p>

---

#  Architecture Overview

The solution follows a layered architecture in which each AWS service performs a dedicated responsibility.

1. Healthcare CSV files are uploaded into an encrypted Amazon S3 raw data bucket.

2. AWS Glue Crawlers automatically scan the uploaded files and populate the AWS Glue Data Catalog with metadata.

3. Amazon Athena queries the cataloged data directly from Amazon S3 without provisioning or managing database servers.

4. Athena CTAS (Create Table As Select) statements create optimized curated datasets stored in a separate encrypted S3 bucket.

5. SQL views provide simplified access to curated healthcare information for reporting and analytics.

6. Amazon CloudWatch collects operational metrics, crawler logs, and Athena query statistics to support observability.

7. AWS CloudTrail records AWS management API activity across the environment for governance and auditing.

8. Amazon EventBridge continuously monitors CloudTrail events and detects predefined security-related administrative actions.

9. Amazon SNS distributes email notifications whenever monitored events occur, enabling real-time operational awareness.

This architecture separates storage, metadata management, analytics, monitoring, auditing, and automation into independent managed services, resulting in a scalable and highly maintainable cloud-native solution.

---

#  AWS Services Used

| AWS Service | Purpose |
|-------------|----------|
| **Amazon S3** | Stores raw and curated healthcare datasets using server-side encryption (SSE-KMS). |
| **AWS Glue Crawler** | Automatically discovers uploaded datasets and creates metadata. |
| **AWS Glue Data Catalog** | Maintains centralized metadata for Athena queries. |
| **Amazon Athena** | Performs serverless SQL analytics directly against S3 data. |
| **Athena CTAS** | Creates optimized curated datasets from raw patient data. |
| **Athena Views** | Simplifies analytical queries using reusable SQL views. |
| **Amazon CloudWatch** | Collects operational metrics, logs, dashboards, and monitoring information. |
| **AWS CloudTrail** | Records AWS management API activity for auditing and governance. |
| **Amazon EventBridge** | Detects predefined CloudTrail events and routes them automatically. |
| **Amazon SNS** | Sends real-time email notifications when monitored events occur. |
| **Amazon EC2** | Provides a test workload used to validate automated security monitoring and event detection. |

---

#  Project Workflow

```text
Healthcare Patient Dataset (CSV)
              │
              ▼
     Amazon S3 (Raw Bucket)
              │
              ▼
      AWS Glue Crawler
              │
              ▼
      AWS Glue Data Catalog
              │
              ▼
        Amazon Athena
              │
              ▼
   Curated Patient Dataset
              │
              ▼
     SQL Views & Analytics
              │
     ┌────────┴────────┐
     ▼                 ▼
CloudWatch         CloudTrail
     │                 │
     └────────┬────────┘
              ▼
        Amazon EventBridge
              │
              ▼
          Amazon SNS
              │
              ▼
     Email Security Alerts
```

The project demonstrates a complete serverless workflow in which data processing, monitoring, governance, and automated alerting are integrated into a single AWS solution.

# 📂 Folder Structure

```text
SentinelLake/
│
├── README.md
│
├── architecture/
│   └── 38-sentinellake-solution-architecture.png
│
├── report/
│   └── SentinelLake_Project_Report.pdf
│
├── screenshots/
│   ├── 01-s3-raw-bucket-overview.png
│   ├── 02-s3-raw-bucket-kms-encryption.png
│   ├── 03-s3-curated-bucket-overview.png
│   ├── ...
│   ├── 37-sns-stopinstances-alert-email.png
│   └── 38-sentinellake-solution-architecture.png
│
└── datasets/
    └── patient_records.csv
```

The repository is intentionally organized to mirror the complete implementation journey of the SentinelLake project.

- **README.md** provides a comprehensive walkthrough of the project, architecture, implementation, and outcomes.
- **architecture/** contains the overall AWS solution architecture used throughout the project.
- **report/** contains the complete project report with detailed explanations and supporting documentation.
- **screenshots/** documents every implementation step in chronological order, allowing the project to be reproduced from start to finish.
- **datasets/** contains the synthetic healthcare dataset used to build the serverless analytics pipeline.

#  Dataset Description

The project uses a synthetic healthcare patient dataset designed to simulate a hospital information system. The dataset contains structured patient records and serves as the input for the complete AWS analytics pipeline.

### Dataset Characteristics

| Feature | Description |
|----------|-------------|
| Format | CSV |
| Record Type | Healthcare patient records |
| Storage | Amazon S3 Raw Bucket |
| Processing | AWS Glue Crawler |
| Query Engine | Amazon Athena |
| Output | Curated analytical table and SQL view |

### Dataset Columns

| Column | Description |
|---------|-------------|
| patient_id | Unique patient identifier |
| hospital | Hospital where the patient received treatment |
| diagnosis | Primary medical diagnosis |
| age | Patient age |
| gender | Patient gender |
| admission_status | Current admission status (Admitted, Discharged, Observation, etc.) |

The dataset was intentionally structured to demonstrate how AWS Glue automatically infers schema information, allowing Athena to query the data without requiring manual database creation.

---

#  Step-by-Step Implementation

The SentinelLake project was developed incrementally across six implementation phases. Each phase introduced additional AWS services and functionality until the complete serverless analytics and monitoring platform was operational.

The screenshots included throughout this section document every major configuration step performed during the project.

---

## Phase 1 — Secure Data Lake Foundation

**Objective**

Build a secure Amazon S3 data lake for storing raw and curated healthcare datasets.

**Services Used**

- Amazon S3
- AWS KMS

**Implementation Summary**

The project began by creating separate Amazon S3 buckets for raw and curated datasets. Both buckets were secured using AWS KMS server-side encryption before uploading the patient dataset to the raw bucket.

### Step 1 — Create Raw S3 Bucket

<p align="center">
<img src="screenshots/01-s3-raw-bucket-overview.png" width="900">
</p>

### Step 2 — Enable KMS Encryption on Raw Bucket

<p align="center">
<img src="screenshots/02-s3-raw-bucket-kms-encryption.png" width="900">
</p>

### Step 3 — Create Curated S3 Bucket

<p align="center">
<img src="screenshots/03-s3-curated-bucket-overview.png" width="900">
</p>

### Step 4 — Enable KMS Encryption on Curated Bucket

<p align="center">
<img src="screenshots/04-s3-curated-bucket-kms-encryption.png" width="900">
</p>

### Step 5 — Configure Athena Query Results Bucket

<p align="center">
<img src="screenshots/05-s3-athena-results-overview.png" width="900">
</p>

### Step 6 — Enable Encryption for Athena Results Bucket

<p align="center">
<img src="screenshots/06-s3-athena-results-kms-encryption.png" width="900">
</p>

### Step 7 — Upload Dataset

<p align="center">
<img src="screenshots/07-patients-data-uploaded-to-raw-bucket.png" width="900">
</p>

**Outcome**

✔ Secure S3 data lake created

✔ KMS encryption enabled

✔ Patient dataset uploaded successfully

---

## Phase 2 — Metadata Discovery

**Objective**

Automatically discover and catalog the uploaded healthcare dataset.

**Services Used**

- AWS Glue
- AWS Glue Data Catalog

**Implementation Summary**

AWS Glue was configured to automatically scan the uploaded CSV dataset, infer its schema, and register metadata inside the Glue Data Catalog.

### Step 8 — Create Glue Database

<p align="center">
<img src="screenshots/08-glue-database-created.png" width="900">
</p>

### Step 9 — Review Glue Crawler Configuration

<p align="center">
<img src="screenshots/09-glue-crawler-review.png" width="900">
</p>

### Step 10 — Create Glue Crawler

<p align="center">
<img src="screenshots/10-glue-crawler-created.png" width="900">
</p>

### Step 11 — Glue Crawler Successfully Configured

<p align="center">
<img src="screenshots/11-glue-crawler-finally-configured.png" width="900">
</p>

**Outcome**

✔ Glue Database created

✔ Glue Crawler configured

✔ Metadata catalog generated automatically

✔ Dataset ready for Athena

---

## Phase 3 — Serverless SQL Analytics

**Objective**

Transform raw healthcare records into curated analytical datasets using Amazon Athena.

**Services Used**

- Amazon Athena
- AWS Glue Data Catalog

**Implementation Summary**

Amazon Athena was configured to query the Glue Catalog. SQL statements were executed to validate the schema, inspect records, build curated tables, and create reusable SQL views.

### Step 12 — Configure Athena Query Results

<p align="center">
<img src="screenshots/12-athena-query-results-configured.png" width="900">
</p>

### Step 13 — Create Athena Results Folder

<p align="center">
<img src="screenshots/13-athena-results-folder-created.png" width="900">
</p>

### Step 14 — Execute First Query

<p align="center">
<img src="screenshots/14-athena-first-query-executed.png" width="900">
</p>

### Step 15 — Review Table Schema

<p align="center">
<img src="screenshots/15-athena-table-schema.png" width="900">
</p>

### Step 16 — Count Dataset Rows

<p align="center">
<img src="screenshots/16-athena-row-count.png" width="900">
</p>

### Step 17 — Create Curated Table

<p align="center">
<img src="screenshots/17-curated-table-created.png" width="900">
</p>

### Step 18 — Review Curated Table

<p align="center">
<img src="screenshots/18-curated-table-listed.png" width="900">
</p>

### Step 19 — Query Curated Table

<p align="center">
<img src="screenshots/19-curated-table-first-query.png" width="900">
</p>

### Step 20 — Create Patient Summary View

<p align="center">
<img src="screenshots/20-patient-summary-view-created.png" width="900">
</p>

### Step 21 — Review Patient Summary View

<p align="center">
<img src="screenshots/21-patient-summary-view-listed.png" width="900">
</p>

### Step 22 — Query Patient Summary View

<p align="center">
<img src="screenshots/22-patient-summary-view-query.png" width="900">
</p>

**Outcome**

✔ Athena configured successfully

✔ Curated analytical table created

✔ SQL view implemented

✔ Serverless analytics operational

---

## Phase 4 — Monitoring and Operational Visibility

**Objective**

Monitor the SentinelLake platform and gain operational visibility into AWS Glue and Amazon Athena activities using Amazon CloudWatch.

**Services Used**

- Amazon CloudWatch
- AWS Glue
- Amazon Athena

**Implementation Summary**

Amazon CloudWatch was configured to monitor the data pipeline. Glue crawler log groups and log streams were reviewed to verify crawler execution, while a custom CloudWatch dashboard was created to visualize Athena query performance metrics.

### Step 23 — Open Amazon CloudWatch

<p align="center">
<img src="screenshots/23-cloudwatch-home.png" width="900">
</p>

### Step 24 — Review CloudWatch Log Groups

<p align="center">
<img src="screenshots/24-cloudwatch-log-groups.png" width="900">
</p>

### Step 25 — Inspect AWS Glue Log Group

<p align="center">
<img src="screenshots/25-cloudwatch-glue-log-group.png" width="900">
</p>

### Step 26 — Review Glue Crawler Log Events

<p align="center">
<img src="screenshots/26-cloudwatch-crawler-logs.png" width="900">
</p>

### Step 27 — Create CloudWatch Monitoring Dashboard

<p align="center">
<img src="screenshots/27-cloudwatch-athena-metrics-dashboard.png" width="900">
</p>

**Outcome**

✔ CloudWatch monitoring configured

✔ Glue crawler execution logs available

✔ Athena performance metrics visualized

✔ Custom monitoring dashboard created

✔ Operational visibility established

---

## Phase 5 — Audit Logging and Event Tracking

**Objective**

Capture and audit AWS management activities using AWS CloudTrail.

**Services Used**

- AWS CloudTrail

**Implementation Summary**

AWS CloudTrail was enabled to record management events across the AWS account. The event history was then reviewed to verify that API activities generated during project implementation were successfully captured.

### Step 28 — Create CloudTrail Trail

<p align="center">
<img src="screenshots/28-cloudtrail-trail-created.png" width="900">
</p>

### Step 29 — Review CloudTrail Event History

<p align="center">
<img src="screenshots/29-cloudtrail-event-history.png" width="900">
</p>

### Step 30 — Configure EventBridge Event Pattern

<p align="center">
<img src="screenshots/30-eventbridge-rule-event-pattern.png" width="900">
</p>

**Outcome**

✔ CloudTrail configured successfully

✔ Management events captured

✔ AWS API activity recorded

✔ Foundation prepared for event-driven automation

---

## Phase 6 — Event-Driven Security Notifications

**Objective**

Automate notifications for critical AWS management events using Amazon EventBridge and Amazon SNS.

**Services Used**

- Amazon EventBridge
- Amazon SNS
- AWS CloudTrail
- Amazon EC2

**Implementation Summary**

An Amazon SNS topic was created and an email subscription was confirmed to receive notifications. An EventBridge rule was then configured to monitor selected CloudTrail management events and publish matching events to the SNS topic. The workflow was validated by stopping a test EC2 instance, which successfully triggered an email notification.

### Step 31 — Create SNS Topic

<p align="center">
<img src="screenshots/31-sns-create-topic.png" width="900">
</p>

### Step 32 — Confirm Email Subscription

<p align="center">
<img src="screenshots/32-Email-subscription-confirmed.png" width="900">
</p>

### Step 33 — Configure SNS as EventBridge Target

<p align="center">
<img src="screenshots/33-EventBridge-is-connected-to-SNS.png" width="900">
</p>

### Step 34 — Create EventBridge Rule

<p align="center">
<img src="screenshots/34-EventBridge-Rule-Successfully-Created.png" width="900">
</p>

### Step 35 — Launch Test EC2 Instance

<p align="center">
<img src="screenshots/35-ec2-instance-running.png" width="900">
</p>

### Step 36 — Stop Test EC2 Instance

<p align="center">
<img src="screenshots/36-ec2-instance-stopped.png" width="900">
</p>

### Step 37 — Receive SNS Email Notification

<p align="center">
<img src="screenshots/37-sns-stopinstances-alert-email.png" width="900">
</p>

**Outcome**

✔ SNS topic created

✔ Email subscription confirmed

✔ EventBridge rule configured

✔ CloudTrail events monitored automatically

✔ SNS email alerts delivered successfully

✔ End-to-end event-driven automation validated

---

---

# Security Features

The SentinelLake platform incorporates multiple AWS security services and best practices to protect data, monitor infrastructure activity, and automate responses to critical events.

### Data Protection

- AWS KMS server-side encryption protects both the raw and curated Amazon S3 buckets.
- Encryption at rest ensures sensitive healthcare data remains protected throughout the analytics pipeline.

### Access Auditing

- AWS CloudTrail records management API activities performed across the AWS account.
- Event history provides a centralized audit trail for security investigations and compliance.

### Event Monitoring

- Amazon EventBridge continuously monitors CloudTrail management events.
- Critical actions such as EC2 instance stops, S3 bucket deletion, and IAM user creation are detected automatically.

### Automated Notifications

- Amazon SNS immediately delivers email notifications whenever monitored security events occur.
- This enables faster incident awareness without requiring continuous manual monitoring.

---

# 📈 Monitoring Features

Amazon CloudWatch was implemented to provide operational visibility into the SentinelLake environment.

The monitoring solution includes:

- AWS Glue crawler execution logs
- CloudWatch Log Groups
- CloudWatch Log Streams
- Athena query performance metrics
- Custom CloudWatch dashboard

The custom dashboard tracks important operational metrics including:

- Processed Bytes
- Total Execution Time
- Engine Execution Time

These metrics help evaluate query performance and provide insight into the health of the analytics pipeline.

<p align="center">
  <img src="screenshots/27-cloudwatch-athena-metrics-dashboard.png" width="900">
</p>

---

#  Event-Driven Automation

One of the key objectives of SentinelLake was to demonstrate an event-driven cloud architecture using native AWS services.

The automation workflow is illustrated below:

```text
CloudTrail
      │
      ▼
EventBridge Rule
      │
      ▼
Amazon SNS Topic
      │
      ▼
Email Notification
```

When a monitored management event occurs, CloudTrail records the API activity.

Amazon EventBridge continuously evaluates CloudTrail events against predefined rules. If a matching event is detected, the event is automatically forwarded to Amazon SNS, which immediately sends an email notification to subscribed users.

The workflow was validated by stopping a test EC2 instance. The event successfully triggered the EventBridge rule, and an email notification was delivered through Amazon SNS.

<p align="center">
  <img src="screenshots/34-EventBridge-Rule-Successfully-Created.png" width="900">
</p>

<p align="center">
  <img src="screenshots/37-sns-stopinstances-alert-email.png" width="900">
</p>

---

# Project Outcomes

The SentinelLake project successfully demonstrates the implementation of a secure, serverless AWS analytics platform capable of ingesting, cataloging, querying, monitoring, auditing, and automating responses to infrastructure events.

Key achievements include:

- Secure Amazon S3 data lake with KMS encryption
- Automated metadata discovery using AWS Glue Crawlers
- Serverless SQL analytics using Amazon Athena
- Curated analytical tables and reusable SQL views
- Operational monitoring through Amazon CloudWatch
- Centralized audit logging with AWS CloudTrail
- Event-driven automation using Amazon EventBridge
- Email notifications through Amazon SNS
- End-to-end validation of the monitoring and alerting workflow

The project showcases how multiple AWS services can be integrated into a production-style data lake architecture while following cloud-native best practices.

# 💡 Skills Demonstrated

This project demonstrates practical experience across multiple AWS services and cloud engineering concepts.

### Cloud Services

- Amazon S3
- AWS Glue
- AWS Glue Data Catalog
- Amazon Athena
- Amazon CloudWatch
- AWS CloudTrail
- Amazon EventBridge
- Amazon SNS
- AWS KMS

### Data Engineering

- Serverless data lake design
- Metadata cataloging
- SQL analytics
- CTAS table creation
- SQL view creation
- Data validation
- Query optimization

### Cloud Operations

- Infrastructure monitoring
- Log analysis
- Performance dashboards
- Audit logging
- Event-driven architecture
- Automated notifications

### Security

- Encryption at rest
- CloudTrail auditing
- Event monitoring
- Operational visibility

# Future Improvements

Potential enhancements for future versions of SentinelLake include:

- Integration with AWS Lambda for automated remediation.
- Amazon QuickSight dashboards for business intelligence and visualization.
- AWS Step Functions for workflow orchestration.
- Amazon Macie for sensitive data discovery.
- Amazon GuardDuty for threat detection.
- Infrastructure deployment using AWS CloudFormation or Terraform.
- CI/CD automation using GitHub Actions.
- Expansion of the healthcare dataset to support larger-scale analytics.

#  Author

**Padmore Nana Prempeh**

Ph.D. Student in Biostatistics  
University at Albany, SUNY

**Areas of Interest**

- Cloud Computing
- Data Engineering
- Machine Learning
- MLOps
- AI Systems Engineering


#  License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this project for educational and personal purposes under the terms of the MIT License.