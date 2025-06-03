# Todo App Architecture on AWS

## Architecture Overview

```
┌─────────────────┐     ┌───────────────────────────────────────────────────────────────┐
│                 │     │                         AWS Cloud                              │
│                 │     │                                                               │
│    Internet     │     │  ┌─────────────┐        ┌─────────────┐      ┌────────────┐  │
│                 │     │  │             │        │             │      │            │  │
│    Users        │◄────┼──┤ CloudFront  │◄───────┤     ALB     │◄─────┤ ECS Tasks  │  │
│                 │     │  │             │        │             │      │            │  │
└─────────────────┘     │  └─────────────┘        └─────────────┘      └────────────┘  │
                        │                                                    │         │
                        │                                                    │         │
                        │                                                    ▼         │
                        │                                           ┌─────────────────┐│
                        │                                           │                 ││
                        │                                           │  ECR Image      ││
                        │                                           │  Repository     ││
                        │                                           │                 ││
                        │                                           └────────┬────────┘│
                        │                                                    │         │
                        │                                                    │         │
                        │                                                    ▼         │
                        │                                           ┌─────────────────┐│
                        │                                           │                 ││
                        │                                           │  CloudWatch     ││
                        │                                           │  Logs           ││
                        │                                           │                 ││
                        │                                           └─────────────────┘│
                        │                                                              │
                        └──────────────────────────────────────────────────────────────┘
```

## Components

1. **CloudFront Distribution**
   - Domain: d12fvnun5dn0t0.cloudfront.net
   - Global content delivery network
   - HTTPS enabled with automatic certificate
   - Caching static assets
   - DDoS protection

2. **Application Load Balancer (ALB)**
   - DNS Name: todo-app-alb-1370593931.us-west-2.elb.amazonaws.com
   - Distributes traffic to ECS tasks
   - Health checks on /health endpoint
   - Security group allows traffic on ports 80 and 443

3. **ECS Service**
   - Cluster: todo-app-cluster
   - Service: todo-app-service
   - Task Definition: todo-app:1
   - Security group only allows traffic from ALB

4. **Container Image**
   - Stored in Amazon ECR
   - Repository: todo-app
   - Node.js application with Express
   - Health check endpoint at /health

5. **Networking**
   - VPC: vpc-066b9767c32711f63
   - Public subnets for ALB
   - Security groups for controlled access

6. **Monitoring**
   - CloudWatch Logs for container logs
   - ALB access logs (optional)
   - CloudFront logs (optional)

## Access URLs

- **CloudFront (Primary Access)**: https://d12fvnun5dn0t0.cloudfront.net
- **ALB (Backend)**: http://todo-app-alb-1370593931.us-west-2.elb.amazonaws.com

## Security Features

1. ECS tasks are not directly accessible from the internet
2. Traffic is encrypted between users and CloudFront
3. Security groups restrict traffic flow
4. AWS Shield Standard provides DDoS protection via CloudFront
