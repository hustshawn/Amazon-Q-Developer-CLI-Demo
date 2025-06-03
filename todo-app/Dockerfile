FROM public.ecr.aws/docker/library/node:20.19.2-slim

# Create app directory
WORKDIR /usr/src/app

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && apt-get clean

# Copy package.json and package-lock.json
COPY package*.json ./

# Install production dependencies only
RUN npm install --production

# Copy app source code
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Add a healthcheck directly in the Dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Command to run the app
CMD ["npm", "start"]
