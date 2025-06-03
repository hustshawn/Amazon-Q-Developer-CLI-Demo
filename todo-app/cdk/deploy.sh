#!/bin/bash
set -e

# Get AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)
if [ -z "$AWS_REGION" ]; then
  AWS_REGION="us-west-2"
fi

echo "Using AWS Account: $AWS_ACCOUNT_ID in region: $AWS_REGION"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install
fi

# Bootstrap CDK (if not already done)
echo "Bootstrapping CDK environment..."
cdk bootstrap

# Deploy the networking stack first
echo "Deploying networking stack..."
cdk deploy TodoAppNetworkingStack --require-approval never

# Deploy the ECS stack (this will automatically build and push the Docker image)
echo "Deploying ECS stack..."
cdk deploy TodoAppEcsStack --require-approval never

# Get the load balancer DNS name
LB_DNS=$(aws cloudformation describe-stacks --stack-name TodoAppEcsStack --query "Stacks[0].Outputs[?OutputKey=='LoadBalancerDNS'].OutputValue" --output text)

echo "Deployment complete!"
echo "You can access your Todo App at: http://$LB_DNS"
echo "Note: It may take a few minutes for the new container to be deployed and become healthy."

# Wait for service to stabilize
echo "Waiting for service to stabilize..."
SERVICE_NAME=$(aws ecs list-services --cluster todo-app-cluster --query "serviceArns[0]" --output text | awk -F'/' '{print $3}')
aws ecs wait services-stable --cluster todo-app-cluster --services $SERVICE_NAME

echo "Service is now stable. Your Todo App should be accessible at: http://$LB_DNS"
