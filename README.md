# ☁️ Legend Cloud Portfolio

Welcome to my Cloud Engineering portfolio.

This repository documents hands-on cloud infrastructure projects built
to strengthen my practical skills in AWS, cloud architecture,
infrastructure engineering, networking, security, and DevOps.

Each project is designed, deployed, tested, and documented with
architecture diagrams, implementation evidence, validation results,
technical reports, and lessons learned.

------------------------------------------------------------------------

## 👨🏾‍💻 About Me

**Padmore Nana Prempeh**

Ph.D. Researcher \| Machine Learning \| Biostatistics \| AI \| Cloud
Engineering

I am building practical cloud infrastructure projects while expanding my
expertise in AWS, DevOps, Data Engineering, and scalable distributed
systems.

My work combines a strong background in statistics, machine learning,
and research with hands-on experience designing and validating cloud
infrastructure.

------------------------------------------------------------------------

## 🏗️ Completed Projects

  -------------------------------------------------------------------------------------------------------------------
  Project                                                       Architecture      Key AWS Services  Status
                                                                Focus                               
  ------------------------------------------------------------- ----------------- ----------------- -----------------
  [AWS Highly Available Web                                     High              EC2, ALB, Auto    ✅ Completed
  Application](projects/aws-01-highly-available-web-app/)       availability,     Scaling,          
                                                                auto healing,     CloudWatch        
                                                                dynamic scaling                     

  [MediVault Cloud: Secure Three-Tier AWS                       Network           VPC, EC2, ALB,    ✅ Completed
  Architecture](projects/aws-02-three-tier-web-architecture/)   segmentation,     NAT Gateway, RDS  
                                                                private           MySQL             
                                                                application tier,                   
                                                                isolated database                   
                                                                tier                                
  -------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 🌟 Featured Project

## MediVault Cloud: Secure Three-Tier AWS Architecture

MediVault Cloud is a secure three-tier web application architecture
deployed on AWS.

The project demonstrates how to design and validate a layered cloud
environment that separates public-facing infrastructure, application
workloads, and database resources into distinct network tiers.

### Architecture Flow

``` text
Internet
   │
   ▼
Internet Gateway
   │
   ▼
Application Load Balancer
   │
   ├───────────────┐
   ▼               ▼
Public Subnet A   Public Subnet B
   │
   ▼
Private Application Tier
   │
   ▼
EC2 Application Server
   │
   ▼
Private Database Tier
   │
   ▼
Amazon RDS for MySQL
```

The architecture was built inside a custom VPC with CIDR block
`10.20.0.0/16` and spans two Availability Zones in the `us-east-1`
Region.

The implementation includes:

-   six subnets across two Availability Zones;
-   public routing through an Internet Gateway;
-   outbound private application routing through a NAT Gateway;
-   an internet-facing Application Load Balancer;
-   an EC2 application server;
-   an Amazon RDS for MySQL database;
-   security-group chaining between architecture tiers;
-   private database subnet isolation;
-   end-to-end browser and database connectivity validation.

### Security Model

``` text
Internet
   │ HTTP : 80
   ▼
ALB Security Group
   │ HTTP : 80
   ▼
Application Security Group
   │ MySQL : 3306
   ▼
Database Security Group
```

The database is not publicly accessible. MySQL traffic is permitted only
from resources associated with the application security group.

### Validation Completed

The deployment was validated by:

-   accessing the application through the Application Load Balancer;
-   confirming the EC2 target passed load balancer health checks;
-   verifying private application-tier routing;
-   testing EC2-to-RDS connectivity on TCP port `3306`;
-   authenticating successfully to MySQL;
-   creating and selecting the application database;
-   creating the `app_users` table;
-   inserting and querying application data.

### Project Documentation

-   [View Project
    README](projects/aws-02-three-tier-web-architecture/README.md)
-   [View Technical
    Report](projects/aws-02-three-tier-web-architecture/report/report.md)
-   [View Implementation
    Evidence](projects/aws-02-three-tier-web-architecture/screenshots/)

------------------------------------------------------------------------

# 🚀 Project 1

## AWS Highly Available Web Application

This project demonstrates the deployment of a production-style highly
available web application architecture on AWS.

The infrastructure uses an Application Load Balancer, an Auto Scaling
Group, multiple EC2 instances, and CloudWatch monitoring to provide
fault tolerance, automatic recovery, and dynamic scaling.

### Capabilities Demonstrated

-   traffic distribution through an Application Load Balancer;
-   deployment across multiple Availability Zones;
-   automatic replacement of unhealthy EC2 instances;
-   dynamic scaling based on CPU utilization;
-   infrastructure monitoring with CloudWatch;
-   deployment of website files through SSH and the Linux command line.

### Project Documentation

-   [View Project
    README](projects/aws-01-highly-available-web-app/README.md)
-   [View Technical
    Report](projects/aws-01-highly-available-web-app/report/report.md)
-   [View Implementation
    Evidence](projects/aws-01-highly-available-web-app/screenshots/)

------------------------------------------------------------------------

## 🛠️ Skills Demonstrated

### AWS Cloud Architecture

-   Amazon VPC
-   Amazon EC2
-   Application Load Balancer
-   Auto Scaling
-   Amazon RDS for MySQL
-   NAT Gateway
-   Internet Gateway
-   Route Tables
-   Security Groups
-   CloudWatch
-   Custom AMIs
-   Launch Templates
-   Target Groups

### Networking and Security

-   VPC CIDR planning
-   Public and private subnet design
-   Multi-AZ architecture
-   Internet routing
-   NAT-based outbound connectivity
-   Network segmentation
-   Security-group chaining
-   Least-privilege traffic control
-   Private database isolation
-   Layered three-tier architecture

### Systems and Tools

-   Linux
-   SSH
-   Apache HTTP Server
-   MySQL client
-   Git
-   GitHub
-   macOS Terminal

------------------------------------------------------------------------

## 📁 Repository Structure

``` text
legend-cloud-portfolio/
│
├── projects/
│   ├── aws-01-highly-available-web-app/
│   │   ├── architecture/
│   │   ├── configs/
│   │   ├── report/
│   │   ├── screenshots/
│   │   └── README.md
│   └── aws-02-three-tier-web-architecture/
│       ├── architecture/
│       ├── configs/
│       ├── report/
│       │   └── report.md
│       ├── screenshots/
│       └── README.md
├── .gitignore
├── index.html
└── README.md
```

------------------------------------------------------------------------

## 📊 Current Progress

  Area                             Progress
  -------------------------------- -----------------
  AWS Cloud Architecture           ✅ Active
  High Availability                ✅ Demonstrated
  Auto Scaling and Auto Healing    ✅ Demonstrated
  VPC Networking                   ✅ Demonstrated
  Three-Tier Architecture          ✅ Demonstrated
  Private Application Networking   ✅ Demonstrated
  RDS Database Integration         ✅ Demonstrated
  Cloud Security                   ✅ Demonstrated
  Docker                           ⏳ In Progress
  Infrastructure as Code           🛠️ Planned
  CI/CD                            🛠️ Planned
  Kubernetes                       🛠️ Planned

------------------------------------------------------------------------

## 🗺️ Roadmap

Future portfolio projects will expand into:

-   Docker containerization
-   Terraform infrastructure as code
-   GitHub Actions and CI/CD
-   Amazon ECS
-   Amazon EKS
-   Kubernetes
-   serverless architecture with AWS Lambda
-   event-driven cloud architecture
-   cloud-based data engineering
-   Apache Airflow
-   Apache Spark
-   Apache Kafka

------------------------------------------------------------------------

## 📫 Contact

**GitHub:**
[Padmore-Nana-Prempeh](https://github.com/Padmore-Nana-Prempeh)

------------------------------------------------------------------------

> This portfolio is continuously developed through hands-on
> implementation. Each project focuses on building, testing,
> troubleshooting, validating, and documenting real cloud
> infrastructure.
