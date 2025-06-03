# AWS CDK rules

- Use L2 Construct when necessary
- Sepearate the foundation resources into a sepearate stack, be careful of the order of dependencies. For example, when deploy an applciation to ECS, networking stack should be created first and then ECS stack; when tear down, ECS stack must be destroy first and then ECS.
- When deploy the ECS stack, make sure the application running. Make sure integrate with the container build process inside of the ECS stack of CDK code.
