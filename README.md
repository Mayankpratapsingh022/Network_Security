# Network Security Project: Malicious URL Detection

This project is focused on detecting malicious URLs using AWS services such as EC2, S3, ECR, and GitHub Actions for CI/CD. The system utilizes Docker for packaging and deployment of the model, which is hosted on an EC2 instance. The project is still in progress.

## Prerequisites

Before starting, ensure you have the following:

- AWS Account
- Docker installed locally (for building the image)
- GitHub repository
- MongoDB instance (optional, for connecting to your database)

## Setup Guide

### Step 1: AWS Console Login

Login to your [AWS Management Console](https://aws.amazon.com/console/) to configure resources like IAM users, S3 buckets, and EC2 instances.

### Step 2: Create IAM User for Deployment

1. Go to the **IAM** service on AWS.
2. Create an IAM user with specific access permissions for:
   - **EC2 Access**: Allows access to virtual machines.
   - **S3 Bucket**: Allows storing artifacts and models.
   - **ECR**: Allows saving Docker images in AWS.

#### IAM Policy Attachments
Attach the following policies to the IAM user:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonEC2FullAccess`
- `AmazonS3FullAccess`

### Step 3: Create an S3 Bucket

Create an S3 bucket to store artifacts and models:

- **Region**: `ap-south-1`
- **Bucket Name**: `malicious-url-detection`

### Step 4: Create ECR Repository

Create an ECR repository to store Docker images:

- **ECR Repository URI**: `566373416292.dkr.ecr.ap-south-1.amazonaws.com/malicious-url`

### Step 5: Setup EC2 Machine

1. Launch an EC2 instance with Ubuntu as the operating system.
2. Once the instance is running, SSH into the machine and install Docker:

```bash
sudo apt-get update -y
sudo apt-get upgrade
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
