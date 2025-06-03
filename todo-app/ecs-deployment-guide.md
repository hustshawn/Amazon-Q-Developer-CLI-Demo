# Deploying Todo App to Amazon ECS

This guide provides step-by-step instructions for deploying the Todo App to Amazon ECS.

## Prerequisites

1. AWS CLI installed and configured with appropriate permissions
2. Docker installed and running locally
3. An AWS account with permissions to create ECS resources

## Step 1: Create an ECR Repository

```bash
aws ecr create-repository --repository-name todo-app --region <your-region>
```

## Step 2: Authenticate Docker to ECR

```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
```

## Step 3: Build and Tag the Docker Image

```bash
docker build -t todo-app .
docker tag todo-app:latest <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/todo-app:latest
```

## Step 4: Push the Image to ECR

```bash
docker push <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/todo-app:latest
```

## Step 5: Create ECS Task Definition

Create a file named `task-definition.json`:

```json
{
  "family": "todo-app",
  "networkMode": "awsvpc",
  "executionRoleArn": "arn:aws:iam::<your-account-id>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "todo-app",
      "image": "<your-account-id>.dkr.ecr.<your-region>.amazonaws.com/todo-app:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 3000,
          "hostPort": 3000,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/todo-app",
          "awslogs-region": "<your-region>",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:3000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512"
}
```

Register the task definition:

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

## Step 6: Create ECS Cluster (if not already created)

```bash
aws ecs create-cluster --cluster-name todo-app-cluster
```

## Step 7: Create CloudWatch Log Group

```bash
aws logs create-log-group --log-group-name /ecs/todo-app --region <your-region>
```

## Step 8: Create Security Group for the ECS Service

```bash
aws ec2 create-security-group --group-name todo-app-sg --description "Security group for Todo App ECS service" --vpc-id <your-vpc-id>

aws ec2 authorize-security-group-ingress --group-id <security-group-id> --protocol tcp --port 3000 --cidr 0.0.0.0/0
```

## Step 9: Create ECS Service

```bash
aws ecs create-service \
  --cluster todo-app-cluster \
  --service-name todo-app-service \
  --task-definition todo-app \
  --desired-count 1 \
  --launch-type FARGATE \
  --platform-version LATEST \
  --network-configuration "awsvpcConfiguration={subnets=[<subnet-id-1>,<subnet-id-2>],securityGroups=[<security-group-id>],assignPublicIp=ENABLED}" \
  --region <your-region>
```

## Step 10: Create Application Load Balancer (Optional)

For a production deployment, you might want to add an Application Load Balancer:

1. Create an ALB
2. Create a target group
3. Create a listener
4. Update the ECS service to use the ALB

## Step 11: Access Your Application

If you're using public subnets with public IPs, you can access your application at:

```
http://<task-public-ip>:3000
```

If you're using an ALB:

```
http://<alb-dns-name>
```

## Monitoring and Troubleshooting

- View CloudWatch logs: AWS Console > CloudWatch > Log Groups > /ecs/todo-app
- Check ECS service events: AWS Console > ECS > Clusters > todo-app-cluster > Services > todo-app-service > Events
- View task details: AWS Console > ECS > Clusters > todo-app-cluster > Tasks

## Cleaning Up

To avoid incurring charges, delete the resources when you're done:

```bash
aws ecs delete-service --cluster todo-app-cluster --service todo-app-service --force
aws ecs delete-cluster --cluster todo-app-cluster
aws ecr delete-repository --repository-name todo-app --force
aws logs delete-log-group --log-group-name /ecs/todo-app
aws ec2 delete-security-group --group-id <security-group-id>
```
