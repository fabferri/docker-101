# Build Dockerfile

The standard name is **Dockerfile** (with a capital D and no file extension). For different environments or purposes, you can use variations like:

- **Dockerfile.dev**
- **Dockerfile.prod**
- **Dockerfile.test**

Create a simple Dockerfile:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
# It creates a local image on your host. 
# The image is stored locally and can be viewed with: docker images
docker build -t myapp .
docker run myapp
```

If you use a custom name for the docker file, specify it with the -f flag:
```bash
docker build -f Dockerfile.dev -t myapp .
```

**install bash in alpine container through Docker file**
Create the Dockerfile:
```dockerfile
FROM alpine

# Update package index and install bash
RUN apk update && apk add bash

# Set bash as the default shell for RUN commands
SHELL ["/bin/bash", "-c"]

# Set bash as the default command when container starts
CMD ["bash"]
```

Create the Dockerfile With additional common tools:
```dockerfile
FROM alpine

# Install bash and other useful utilities
# --no-cache - keeps image size smaller
RUN apk add --no-cache \
    bash \
    bash-completion \
    curl \
    vim

#  starts bash when container runs
CMD ["bash"]
```

```bash
# It builds a Docker image from a Dockerfile in the current directory:
docker build -t my-alpine-bash .

# Build with no cache
docker build --no-cache -t my-alpine-bash .

# Run interactively
docker run -it my-alpine-bash

# Run with a custom name
docker run -it --name my-container my-alpine-bash

# Run with volume mount
docker run -it -v $(pwd):/app my-alpine-bash

# Run in background
docker run -d --name my-container my-alpine-bash

# Run and remove after exit
docker run -it --rm my-alpine-bash
```


**More Dockerfile examples:**

**Node.js Application:**
```dockerfile
FROM node:18-alpine
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

**Multi-stage build (smaller final image):**
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm install --production
CMD ["node", "dist/index.js"]
```

## Advanced Docker build commands

```bash
# Build with a specific tag
docker build -t myapp:v1.0 .

# Build with build arguments
docker build --build-arg NODE_ENV=production -t myapp .

# Build with no cache
# --no-cache - forces Docker to rebuild every layer from scratch, ignoring any cached layers
# When to use --no-cache:
#   When you want to ensure you get the latest package updates (e.g., apt-get update)
#   When debugging build issues and you suspect stale cache is the problem
#   When you've made changes outside the Dockerfile that Docker can't detect
docker build --no-cache -t myapp .

# Build from a different Dockerfile
docker build -f Dockerfile.dev -t myapp-dev .

# Build and tag multiple versions
docker build -t myapp:latest -t myapp:v1.0 .

# View build history
docker history myapp
```

---
## Next step

[Docker networking](04-docker-networking.md)

## Coming back

[Docker 101: first trek](README.md)