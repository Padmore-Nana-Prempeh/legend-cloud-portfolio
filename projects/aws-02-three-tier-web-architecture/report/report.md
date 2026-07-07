# MediVault Cloud Technical Report

## Project Overview

**Project name:** MediVault Cloud  
**Project type:** AWS secure three-tier cloud architecture  
**Region:** US East (N. Virginia), `us-east-1`  
**VPC CIDR:** `10.20.0.0/16`

MediVault Cloud is a hands-on AWS architecture project designed to model a secure, layered web application environment. The project demonstrates network segmentation, controlled traffic flow, load balancing, database isolation, and validation through browser and database testing.

The build uses a custom VPC, six subnets across two Availability Zones, public routing through an Internet Gateway, outbound private routing through a NAT Gateway, layered security groups, an Application Load Balancer, an EC2 application server, and an Amazon RDS MySQL database.

---

## Architecture Summary

The intended production architecture follows this flow:

```text
Internet
   |
Internet Gateway
   |
Application Load Balancer
   |
EC2 Application Tier
   |
Amazon RDS MySQL Database Tier
```

The final architecture includes:

- Custom VPC: `project-two-vpc`
- Public subnets:
  - `project-two-public-subnet-a`
  - `project-two-public-subnet-b`
- Private application subnets:
  - `project-two-private-app-subnet-a`
  - `project-two-private-app-subnet-b`
- Private database subnets:
  - `project-two-private-db-subnet-a`
  - `project-two-private-db-subnet-b`
- Internet Gateway: `project-two-igw`
- NAT Gateway: `project-two-nat-a`
- Application Load Balancer: `project-two-alb`
- Target Group: `project-two-app-tg`
- EC2 application instance: `project-two-ec2`
- RDS MySQL database: `project-two-mysql-db`

![Architecture Diagram](../screenshots/30-project-two-medivault-cloud-architecture-diagram.png)

---

## Important Implementation Note

The target production design places the EC2 application server in the private application tier. During this lab implementation, the working EC2 instance was launched in `project-two-public-subnet-a` to simplify SSH access and testing.

This is documented honestly as a lab-stage implementation choice. A production hardening step would be to move the EC2 application server into a private application subnet and use AWS Systems Manager Session Manager or a bastion host for administrative access.

Evidence:

![EC2 Running in Public Subnet](../screenshots/18-ec2-instance-running-in-public-subnet.png)

---

## Network Design

### VPC

A custom VPC was created with CIDR block `10.20.0.0/16`.

![Custom VPC Created](../screenshots/01-custom-vpc-created.png)

### Subnet Layout

Six subnets were created across two Availability Zones.

| Tier | Subnet | CIDR | Availability Zone |
|---|---|---:|---|
| Public | `project-two-public-subnet-a` | `10.20.1.0/24` | `us-east-1a` |
| Public | `project-two-public-subnet-b` | `10.20.2.0/24` | `us-east-1b` |
| Private App | `project-two-private-app-subnet-a` | `10.20.11.0/24` | `us-east-1a` |
| Private App | `project-two-private-app-subnet-b` | `10.20.12.0/24` | `us-east-1b` |
| Private DB | `project-two-private-db-subnet-a` | `10.20.21.0/24` | `us-east-1a` |
| Private DB | `project-two-private-db-subnet-b` | `10.20.22.0/24` | `us-east-1b` |

![Six Subnets Created](../screenshots/02-six-tiered-subnets-created.png)

---

## Internet Access and Routing

### Internet Gateway

An Internet Gateway was created and attached to the custom VPC to allow internet-facing resources to communicate with the public internet.

![Public Route to Internet Gateway](../screenshots/03-public-route-to-internet-gateway.png)

### Public Route Table

The public route table was configured with:

```text
Destination: 0.0.0.0/0
Target: Internet Gateway
```

The two public subnets were explicitly associated with the public route table.

![Public Subnets Associated](../screenshots/04-public-subnets-associated-with-route-table.png)

### Private Database Route Table

The private database subnets were associated with a separate private database route table. This route table does not include a public internet route, keeping the database tier isolated.

![Private DB Subnets Associated](../screenshots/05-private-db-subnets-associated-with-route-table.png)

![Private DB Route Isolation](../screenshots/10-private-db-route-table-isolation.png)

### NAT Gateway

A NAT Gateway was created in the public subnet to allow private application resources to initiate outbound internet traffic without accepting inbound internet connections.

![NAT Gateway Available](../screenshots/08-nat-gateway-a-available.png)

The private application route table was updated to send outbound traffic to the NAT Gateway.

![Private App Route to NAT Gateway](../screenshots/09-private-app-route-to-nat-gateway.png)

The private application subnets were associated with the private application route table.

![Private App Subnets Associated](../screenshots/19-private-app-subnets-associated-with-route-table.png)

---

## Public IP Configuration

Auto-assign public IPv4 was enabled for both public subnets.

![Public Subnet A Auto Assign IPv4](../screenshots/06-public-subnet-a-auto-assign-ipv4-enabled.png)

![Public Subnet B Auto Assign IPv4](../screenshots/07-public-subnet-b-auto-assign-ipv4-enabled.png)

---

## Security Group Design

The security model was built using layered security groups.

### ALB Security Group

Security group: `project-two-alb-sg`

Purpose:

```text
Allow public HTTP traffic to the Application Load Balancer.
```

Inbound rule:

```text
HTTP 80 from 0.0.0.0/0
```

![ALB Security Group Public HTTP Rule](../screenshots/11-alb-security-group-public-http-rule.png)

### Application Security Group

Security group: `project-two-app-sg`

Purpose:

```text
Allow HTTP traffic from the Application Load Balancer only.
```

Inbound rule:

```text
HTTP 80 from project-two-alb-sg
```

![App Security Group ALB Only Rule](../screenshots/12-app-security-group-alb-only-rule.png)

![App Security Group Configuration](../screenshots/13-db-security-group-app-only-configuration.png)

### Database Security Group

Security group: `project-two-db-sg`

Purpose:

```text
Allow MySQL traffic from application servers only.
```

Inbound rule:

```text
MYSQL/Aurora 3306 from project-two-app-sg
```

![DB Security Group Created](../screenshots/15-rds-db-subnet-group-created.png)

![RDS Security Group App Only Rule](../screenshots/16-rds-security-group-app-only-rule.png)

---

## EC2 Application Server

An EC2 instance named `project-two-ec2` was launched using Amazon Linux 2023 and a `t3.micro` instance type.

Key pair:

```text
project-two-key-pair
```

The EC2 instance was attached to `project-two-app-sg`.

![EC2 Network and Security Configuration](../screenshots/17-ec2-network-and-security-group-configuration.png)

![EC2 App Security Group ALB Only Rule](../screenshots/23-ec2-app-security-group-alb-only-rule.png)

---

## Application Server Setup

Apache HTTP Server was installed and started on the EC2 instance.

The test web page returned:

```text
Project Two App Server is running
```

![Application Load Balancer Browser Test](../screenshots/22-application-load-balancer-browser-test-success.png)

---

## Application Load Balancer

An internet-facing Application Load Balancer named `project-two-alb` was created across both public subnets.

The ALB listener was configured as:

```text
Protocol: HTTP
Port: 80
Default action: Forward to project-two-app-tg
```

![Target Group Created](../screenshots/21-target-group-ec2-instance-healthy.png)

![Application Load Balancer Test Success](../screenshots/22-application-load-balancer-browser-test-success.png)

---

## Target Group

Target group: `project-two-app-tg`

Configuration:

```text
Target type: Instance
Protocol: HTTP
Port: 80
Health check path: /
```

The EC2 instance was registered as a target. After Apache was installed and the application test page was available, the target group health check passed.

![Target Group Healthy](../screenshots/21-target-group-ec2-instance-healthy.png)

---

## RDS MySQL Database

An Amazon RDS MySQL database named `project-two-mysql-db` was created in private database subnets.

Database configuration:

```text
Engine: MySQL Community
Instance class: db.t4g.micro
DB identifier: project-two-mysql-db
Private DB subnet group: project-two-db-subnet-group
Security group: project-two-db-sg
```

![RDS DB Subnet Group Created](../screenshots/15-rds-db-subnet-group-created.png)

![RDS MySQL Instance Available](../screenshots/20-rds-mysql-instance-available.png)

---

## Database Connectivity Testing

The MySQL/MariaDB client was installed on the EC2 instance.

![MySQL Client Installed](../screenshots/24-mysql-client-installed-on-ec2.png)

Connectivity from EC2 to RDS over port `3306` was tested successfully.

![EC2 to RDS Port 3306 Connectivity Success](../screenshots/25-ec2-to-private-rds-port-3306-connectivity-success.png)

The EC2 instance successfully connected to the RDS MySQL database.

![EC2 to RDS MySQL Connection Success](../screenshots/26-ec2-to-private-rds-mysql-connection-success.png)

---

## Database Implementation

Inside RDS MySQL, a project database was created:

```sql
CREATE DATABASE project_two_db;
USE project_two_db;
```

![RDS Database Created and Selected](../screenshots/27-rds-database-created-and-selected.png)

A table named `app_users` was created:

```sql
CREATE TABLE app_users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

![RDS App Users Table Created](../screenshots/28-rds-app-users-table-created.png)

Sample records were inserted and verified:

```sql
INSERT INTO app_users (name, email)
VALUES
('Ama Mensah', 'ama@example.com'),
('Kwame Asante', 'kwame@example.com'),
('Akosua Boateng', 'akosua@example.com');

SELECT * FROM app_users;
```

![RDS App Users Data Inserted and Verified](../screenshots/29-rds-app-users-data-inserted-and-verified.png)

---

## Validation Results

| Validation Area | Result |
|---|---|
| VPC created | Successful |
| Six subnets created | Successful |
| Internet Gateway attached | Successful |
| Public route table configured | Successful |
| Private route tables configured | Successful |
| NAT Gateway available | Successful |
| ALB security group created | Successful |
| App security group restricted to ALB | Successful |
| DB security group restricted to app tier | Successful |
| EC2 instance running | Successful |
| Apache web server running | Successful |
| ALB browser test | Successful |
| Target group health check | Healthy |
| RDS MySQL available | Successful |
| EC2-to-RDS port 3306 test | Successful |
| MySQL login from EC2 | Successful |
| Database/table/data creation | Successful |

---

## Security Considerations

This architecture applies several security practices:

1. The database is placed in private database subnets.
2. The database security group only allows MySQL traffic from the application security group.
3. The application security group only allows HTTP traffic from the ALB security group.
4. The ALB is the public entry point for web traffic.
5. Private subnets use NAT Gateway for outbound access instead of direct inbound internet access.
6. Public and private routing responsibilities are separated by route tables.

---

## Known Lab Limitation

The EC2 instance was launched in a public subnet during the lab implementation. This helped with direct SSH access and troubleshooting.

For a more production-ready version, the EC2 application server should be moved into a private application subnet. Administrative access should be handled through AWS Systems Manager Session Manager, a bastion host, or VPN-based private access.

---

## Production Improvement Roadmap

Recommended next improvements:

1. Move EC2 application server into private application subnet.
2. Add AWS Systems Manager Session Manager for secure access.
3. Add HTTPS listener on the ALB using AWS Certificate Manager.
4. Add Route 53 DNS record for a custom domain.
5. Enable RDS automated backups and deletion protection.
6. Enable CloudWatch logs and alarms.
7. Add IAM roles instead of long-lived credentials.
8. Add Terraform or CloudFormation for Infrastructure as Code.
9. Add a second NAT Gateway for higher availability.
10. Replace the simple Apache test page with a real backend application.

---

## Lessons Learned

This project strengthened practical understanding of:

- VPC design
- Public and private subnet separation
- Route table design
- Internet Gateway and NAT Gateway routing
- Security group chaining
- Application Load Balancer setup
- Target group health checks
- EC2 application server configuration
- RDS MySQL deployment
- Database connectivity testing
- Cloud architecture documentation

---

## Final Outcome

MediVault Cloud successfully demonstrates a secure three-tier AWS architecture with working web and database layers. The project shows how internet traffic reaches an Application Load Balancer, how the ALB forwards traffic to an EC2 application server, and how the application tier can securely connect to a private RDS MySQL database.

This project is suitable for a cloud engineering, DevOps, or infrastructure portfolio because it documents not only the final build, but also the architecture decisions, security boundaries, validation steps, and production improvement roadmap.
