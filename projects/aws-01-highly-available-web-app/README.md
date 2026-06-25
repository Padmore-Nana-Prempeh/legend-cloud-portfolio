# AWS Highly Available Web Application

## Project Overview

This project demonstrates the design and deployment of a highly available web application on Amazon Web Services (AWS). The infrastructure was built to provide fault tolerance, automatic recovery, and dynamic scaling while following cloud engineering best practices.

The application is deployed across multiple Availability Zones using an Application Load Balancer (ALB), an Auto Scaling Group (ASG), and multiple EC2 instances. CloudWatch monitors the infrastructure and automatically launches or terminates EC2 instances based on CPU utilization and health checks.

This project was built as part of my AWS Cloud Engineering learning journey and demonstrates practical experience with designing resilient cloud infrastructure rather than deploying a single virtual machine.

---

## Project Objectives

- Deploy a static portfolio website on Amazon EC2.
- Distribute incoming traffic using an Application Load Balancer.
- Achieve high availability across multiple Availability Zones.
- Automatically replace unhealthy EC2 instances.
- Automatically scale the application based on CPU utilization.
- Monitor infrastructure using Amazon CloudWatch.
- Gain hands-on experience with production-style AWS architecture.

---

# Architecture

## High-Level Architecture

```text
                     Internet
                         │
                         ▼
             Application Load Balancer
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
 Availability Zone A              Availability Zone B
        │                               │
        ▼                               ▼
     EC2 Instance                   EC2 Instance
        │                               │
        └───────────────┬───────────────┘
                        ▼
               Auto Scaling Group
                        │
                        ▼
                 Amazon CloudWatch
```

The Application Load Balancer distributes incoming HTTP requests across EC2 instances deployed in multiple Availability Zones.

The Auto Scaling Group continuously monitors the health of the instances. If an instance becomes unhealthy, it is automatically terminated and replaced with a new healthy instance.

Amazon CloudWatch monitors infrastructure metrics such as CPU utilization. When CPU usage exceeds the configured threshold, the Auto Scaling Group automatically launches additional EC2 instances. When utilization decreases, unnecessary instances are terminated to optimize cost.


---

# AWS Services Used

| AWS Service | Purpose in the Project |
|-------------|------------------------|
| Amazon EC2 | Hosted the portfolio web application using Apache on Amazon Linux 2023. |
| Application Load Balancer (ALB) | Distributed incoming HTTP traffic across multiple EC2 instances. |
| Target Group | Registered healthy EC2 instances and routed traffic only to healthy targets. |
| Auto Scaling Group (ASG) | Maintained the desired number of EC2 instances and automatically replaced unhealthy instances. |
| Launch Template | Standardized the EC2 configuration including AMI, instance type, security groups, key pair, and bootstrap script. |
| Amazon CloudWatch | Collected CPU utilization metrics and triggered Auto Scaling policies. |
| Security Groups | Controlled inbound HTTP and SSH access to the EC2 instances and Load Balancer. |
| Virtual Private Cloud (VPC) | Provided network isolation for the application infrastructure. |
| Public Subnets | Hosted the Application Load Balancer and EC2 instances across multiple Availability Zones. |

---

# Infrastructure Components

## EC2 Instances

- Amazon Linux 2023
- Apache HTTP Server
- Bootstrap installation using User Data
- t3.micro instance type
- Deployed in multiple Availability Zones

## Application Load Balancer

- Internet-facing
- Listener on Port 80 (HTTP)
- Routes traffic to the Target Group
- Performs health checks before forwarding requests

## Target Group

- Health check protocol: HTTP
- Health check path: `/`
- Registers only healthy EC2 instances
- Automatically removes unhealthy targets

## Auto Scaling Group

- Desired Capacity: **2**
- Minimum Capacity: **2**
- Maximum Capacity: **4**
- Spans two Availability Zones
- Automatically replaces unhealthy EC2 instances

## CloudWatch

- Monitors Average CPU Utilization
- Target Tracking Policy: **50% CPU**
- Launches additional EC2 instances during high load
- Terminates unnecessary instances when utilization decreases

---

# Deployment Process

This project was built incrementally to simulate a real-world cloud deployment.

## Step 1 — Launch an EC2 Instance

- Launched an Amazon Linux 2023 EC2 instance.
- Configured the Security Group to allow:
  - SSH (Port 22)
  - HTTP (Port 80)
- Connected using SSH from the local terminal.

Example:

```bash
ssh -i legend-key.pem ec2-user@<public-ip>
```

---

## Step 2 — Install Apache

Updated the server and installed Apache.

```bash
sudo dnf update -y
sudo dnf install httpd -y
sudo systemctl enable httpd
sudo systemctl start httpd
```

Verified the web server by visiting the EC2 Public IP.

---

## Step 3 — Deploy the Portfolio Website

Copied the HTML portfolio to:

```
/var/www/html/
```

Verified that the website was publicly accessible.

---

## Step 4 — Create an AMI

Created an Amazon Machine Image (AMI) from the configured EC2 instance.

The AMI became the golden image used for all future Auto Scaling instances.

---

## Step 5 — Create a Launch Template

Configured a Launch Template using:

- Amazon Linux 2023 AMI
- t3.micro instance
- Existing Security Group
- Existing Key Pair
- User Data bootstrap script

This Launch Template ensures every new EC2 instance is configured identically.

---

## Step 6 — Create a Target Group

Created an HTTP Target Group.

Configuration included:

- Protocol: HTTP
- Port: 80
- Health Check Path: /

Only healthy EC2 instances receive traffic.

---

## Step 7 — Create the Application Load Balancer

Configured an Internet-facing Application Load Balancer.

The Load Balancer:

- listens on Port 80
- distributes traffic
- performs health checks
- forwards requests to healthy targets

---

## Step 8 — Create the Auto Scaling Group

Created an Auto Scaling Group using the Launch Template.

Configuration:

- Minimum Capacity: 2
- Desired Capacity: 2
- Maximum Capacity: 4

Instances are distributed across multiple Availability Zones.

---

## Step 9 — Configure Dynamic Scaling

Created a Target Tracking Policy.

Metric:

- Average CPU Utilization

Target Value:

- 50%

When CPU utilization increases, additional EC2 instances are automatically launched.

When CPU utilization decreases, unnecessary instances are terminated.

---

## Step 10 — Validate Auto Healing

Stopped one EC2 instance manually.

The Auto Scaling Group detected the unhealthy instance and automatically:

- terminated it
- launched a replacement
- attached it to the Target Group

This demonstrated automatic recovery without manual intervention.

---

## Step 11 — Validate Dynamic Scaling

Generated CPU load on the EC2 instances.

CloudWatch detected increased utilization.

The Auto Scaling Group automatically increased capacity from:

```
2 → 3 → 4 instances
```

When utilization returned to normal, Auto Scaling reduced capacity while maintaining the minimum required instances.



---

# Testing & Validation

The infrastructure was tested after deployment to verify high availability, automatic recovery, and dynamic scaling.

## Test 1 — Web Application Accessibility

**Objective**

Verify that the Application Load Balancer successfully serves the portfolio website.

**Result**

- Website loaded successfully through the Load Balancer DNS.
- HTTP requests were distributed to healthy EC2 instances.

**Status**

 Passed

---

## Test 2 — Target Group Health Checks

**Objective**

Verify that only healthy EC2 instances receive traffic.

**Result**

- Health checks returned successful responses.
- All healthy instances were automatically registered.

**Status**

 Passed

---

## Test 3 — Auto Healing

**Objective**

Verify that Auto Scaling automatically replaces unhealthy instances.

**Procedure**

- One EC2 instance was manually stopped.

**Observed Result**

- Health check failed.
- Instance was removed from the Target Group.
- Auto Scaling launched a replacement instance.
- Replacement instance became healthy automatically.

**Status**

 Passed

---

## Test 4 — Dynamic Scaling

**Objective**

Verify that Auto Scaling responds to increased CPU utilization.

**Procedure**

Generated CPU load using:

```bash
yes > /dev/null
```

**Observed Result**

CloudWatch detected increased CPU utilization.

Auto Scaling increased capacity:

```
2 → 3 → 4 EC2 instances
```

After CPU utilization returned to normal, the Auto Scaling Group reduced the number of running instances while maintaining the minimum capacity.

**Status**

 Passed

---

## Test 5 — Load Balancer Distribution

**Objective**

Verify that the Application Load Balancer distributes requests across multiple Availability Zones.

**Observed Result**

Requests were successfully routed to healthy EC2 instances in different Availability Zones.

**Status**

 Passed