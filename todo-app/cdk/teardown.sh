#!/bin/bash
set -e

echo "Starting teardown process..."

# Step 1: Scale down the ECS service to 0 tasks
echo "Scaling down ECS service to 0 tasks..."
CLUSTER_NAME="todo-app-cluster"
SERVICE_NAME=$(aws ecs list-services --cluster $CLUSTER_NAME --query "serviceArns[0]" --output text | awk -F'/' '{print $3}')

if [ ! -z "$SERVICE_NAME" ] && [ "$SERVICE_NAME" != "None" ]; then
  echo "Updating service $SERVICE_NAME to desired count 0..."
  aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --desired-count 0 --region us-west-2
  
  # Wait for tasks to be stopped
  echo "Waiting for tasks to stop..."
  aws ecs wait services-stable --cluster $CLUSTER_NAME --services $SERVICE_NAME --region us-west-2
  echo "All tasks stopped."
else
  echo "No ECS service found in cluster $CLUSTER_NAME"
fi

# Step 2: Delete the ECS stack first
echo "Deleting ECS stack..."
cdk destroy TodoAppEcsStack --force

# Step 3: Delete the networking stack
echo "Deleting networking stack..."
cdk destroy TodoAppNetworkingStack --force

echo "Teardown process completed successfully."
