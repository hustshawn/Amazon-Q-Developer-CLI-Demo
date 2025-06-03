FROM node:20-slim as backend-builder
WORKDIR /usr/src/app/backend
COPY backend/package*.json ./
RUN npm install
COPY backend ./

FROM node:20-slim as frontend-builder
WORKDIR /usr/src/app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend ./
RUN npm run build

FROM node:20-slim
WORKDIR /usr/src/app
COPY --from=backend-builder /usr/src/app/backend ./backend
COPY --from=frontend-builder /usr/src/app/frontend/build ./frontend/build

# Install serve to serve the frontend
RUN npm install -g serve

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && apt-get clean

WORKDIR /usr/src/app/backend
EXPOSE 3001
EXPOSE 3000

# Start both backend and frontend
CMD ["sh", "-c", "node app.js & serve -s ../frontend/build -l 3000"]
