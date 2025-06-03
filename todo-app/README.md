# Todo App with React and Express

A modern todo application built with React frontend and Express backend.

## Features

- Add new todos
- Mark todos as completed
- Delete todos
- Responsive design
- Modern React components
- RESTful API backend

## Project Structure

- `frontend/` - React frontend application
- `backend/` - Express backend API
- `cdk/` - AWS CDK deployment code
- `Dockerfile` - Docker configuration for containerization
- `docker-compose.yml` - Docker Compose configuration for local development

## Local Development

### Running with Docker Compose

1. Build and start the containers:
   ```
   docker-compose up --build
   ```

2. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:3001/api/todos

### Running Separately

#### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. The API will be available at http://localhost:3001

#### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

4. The application will be available at http://localhost:3000

## API Endpoints

- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/:id/toggle` - Toggle todo completion status
- `DELETE /api/todos/:id` - Delete a todo
- `GET /health` - Health check endpoint

## Deployment

The application can be deployed to AWS using the CDK code in the `cdk/` directory.

1. Navigate to the CDK directory:
   ```
   cd cdk
   ```

2. Deploy the application:
   ```
   ./deploy.sh
   ```

3. To tear down the infrastructure:
   ```
   ./teardown.sh
   ```

## Technologies Used

- **Frontend**:
  - React
  - CSS
  - Fetch API

- **Backend**:
  - Node.js
  - Express
  - RESTful API

- **DevOps**:
  - Docker
  - AWS CDK
  - AWS ECS
  - AWS ECR
