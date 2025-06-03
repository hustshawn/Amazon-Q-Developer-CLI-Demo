# Todo App CDK Infrastructure

This directory contains the AWS CDK code for deploying the Todo App to AWS.

## Architecture

The infrastructure is split into two separate stacks to manage dependencies properly:

1. **Networking Stack (`TodoAppNetworkingStack`)**
   - VPC with public and private subnets
   - Security groups for the ECS service and load balancer
   - NAT Gateway for outbound internet access from private subnets

2. **ECS Stack (`TodoAppEcsStack`)**
   - ECS cluster
   - Fargate service and task definition
   - Application Load Balancer
   - ECR repository for the Docker image
   - IAM roles and policies
   - CloudWatch logs

This separation ensures that:
- During deployment, the networking infrastructure is created before the ECS resources
- During teardown, the ECS resources are removed before the networking infrastructure

## Prerequisites

- AWS CLI configured with appropriate credentials
- Node.js and npm installed
- Docker installed and running
- AWS CDK installed globally (`npm install -g aws-cdk`)

## Deployment Instructions

### Automated Deployment

Run the deployment script:

```bash
./deploy.sh
```

This script will:
1. Deploy the networking stack first
2. Deploy the ECS stack (which depends on the networking stack)
3. Build and push the Docker image automatically as part of the CDK deployment
4. Wait for the service to stabilize
5. Output the URL to access your application

## Cleanup

To delete all resources created by this stack:

```bash
./teardown.sh
```

This script will:
1. Scale down the ECS service to 0 tasks
2. Wait for all tasks to stop
3. Delete the ECS stack first
4. Then delete the networking stack

## Key Features

1. **Multi-Stack Architecture**: Proper separation of networking and application resources
2. **Integrated Container Build**: Docker image is built and pushed automatically during deployment
3. **Public IP Assignment**: Tasks have public IPs assigned to access the internet
4. **Health Check Configuration**: Proper health check configuration using the `/health` endpoint
5. **Dependency Management**: Stacks are created and deleted in the correct order
