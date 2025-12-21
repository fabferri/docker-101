# your first step with Docker

This article provides your first hands-on steps with Docker, with basic commands to building and deploying containers. It assumes you have already installed Docker Engine on your system.

## Table of Contents

- [Verify the installation](#verify-the-installation)
- [Understand the Docker components](#understand-the-docker-components)
- [Create a Docker group (Linux only)](#create-a-docker-group-linux-only)
- [Pull a real image](#pull-a-real-image)
- [Run and manage containers](#run-and-manage-containers)
- [Creation of multiple containers](#creation-of-multiple-containers)
- [Learn volume mounts and ports](#learn-volume-mounts-and-ports)
- [Build your first Dockerfile](#build-your-first-dockerfile)
- [Install Docker Compose](#install-docker-compose)
- [Configure your workflow](#configure-your-workflow)
- [Security & hygiene best practices (early!)](#security--hygiene-best-practices-early)
- [Docker networking basics](#docker-networking-basics)
- [Useful debugging commands](#useful-debugging-commands)
- [Common Docker workflows](#common-docker-workflows)

---

## Verify the installation
Confirm Docker is installed and running.

```bash
docker --version
docker info
```
`docker --version` → confirms CLI installation
`docker version` → shows the version of docker client and docker server 
`docker info` → confirms the Docker daemon is running


**Run a test container (sanity check)**

```bash
docker run hello-world
```
Initally docker image is not available locally. Docker pulls the image from the Docker Hub, creates the container, and executes it — successful execution indicates a healthy environment.

## Understand the Docker components

Before going further, make sure these concepts are clear:

- Image – immutable template (e.g. nginx, python:3.11)
- Container – running (or stopped) instance of an image
- Dockerfile – recipe to build images
- Registry – where images live (Docker Hub, ACR, ECR, etc.)


## Create a Docker group (Linux only)

- The docker daemon binds to a Unix socket instead of a TCP port. By default that Unix socket (/var/run/docker.sock) is owned by the user root and other users can access it with sudo. For this reason, docker daemon always runs as the root user.
- To avoid having to use sudo when you use the docker command, create a Unix group called docker and add users to it. When the docker daemon starts, it makes the ownership of the Unix socket read/writable by the docker group.

> [Note]
> Adding a user to the docker group is equivalent to granting root access, since they can run containers with full host access.
>

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Pull a real image
Try pulling something meaningful for your work from docker Hub:

```bash
docker pull nginx
docker pull python:3.11
```

List images:
```bash
docker images
```

## Run and manage containers

Run a container interactively:
```bash
docker run -it ubuntu bash
```
To exit from the container just run `exit` or `CTRL+D` <br>
The same command with specify the bash path: `docker run -it ubuntu /bin/bash`

**More interactive examples:**
```bash
# Run Python interpreter interactively
docker run -it python:3.11 python

# Run Alpine Linux (very lightweight)
docker run -it alpine sh
# Note: alpine image doesn't manage bash.
# Install bash inside the alpine container
docker run -it alpine sh
apk add bash
bash

# Run container with a specific name
docker run -it --name myubuntu ubuntu bash
```

Run a container in the background:
```bash
docker run -d -p 8080:80 nginx
```

**Running redis in background container:**
```bash
# Run Redis in background
docker run -d --name redis-server redis
# 1. Check container status:
docker ps
# 2. View Redis logs:
docker logs redis-server
# 3. Connect to Redis CLI:
docker exec -it redis-server redis-cli
#4. Test with a PING command:
docker exec -it redis-server redis-cli ping
# Should return: PONG

# 5. Run the quickest way to verify Redis is working properly:
# Set a value
docker exec -it redis-server redis-cli SET mykey "Hello"

# Get the value
docker exec -it redis-server redis-cli GET mykey
# Should return: "Hello"
```

```bash
# 
# Run MongoDB with environment variables
#   docker run -d - runs container in detached mode (background)
#   --name mongodb - names the container "mongodb"
#   -e MONGO_INITDB_ROOT_USERNAME=admin - sets environment variable for MongoDB admin username
#   -e MONGO_INITDB_ROOT_PASSWORD=password - sets environment variable for MongoDB admin password
#   mongo - the MongoDB image to use
# NOTE: before running the command are required environment variables for initializing MongoDB with root credentials.
docker run -d --name mongodb -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=password mongo
```

```bash
# Runs an Nginx container in the background with automatic restart behavior.
# What each part of command does:
#   docker run - creates and starts a new container
#   -d - detached mode (runs in background)
#   --restart=unless-stopped - restart policy that:
#     Automatically restarts the container if it crashes or exits unexpectedly
#     Restarts the container after Docker daemon restarts (e.g., system reboot)
#     Won't restart if you manually stopped it with docker stop
#   nginx - the image to use
# Other restart policies:
#    no - never restart (default)
#    always - always restart, even if manually stopped
#    on-failure - restart only if container exits with non-zero status
#    on-failure:5 - restart max 5 times on failure
docker run -d --restart=unless-stopped nginx

# Run container with resource limits
docker run -d --memory="512m" --cpus="1.0" nginx
```

Useful commands to know:

`docker ps`               # running containers
`docker ps -a`            # list all containers (includes containers that are stopped)
`docker ps -q`            # list container IDs only (useful for scripting)
`docker logs <id>`        # view container logs
`docker logs -f <id>`     # follow logs in real-time
`docker stop <id>`        # stop a running container
`docker start <id>`       # start a stopped container
`docker restart <id>`     # restart a container
`docker rm <id>`          # remove a container
`docker rm -f <id>`       # force remove a running container
`docker images`           # list of images stored locally
`docker rmi <image>`      # remove an image
`docker inspect <id>`     # detailed container information
`docker exec -it <id> bash` # execute a command in a running container
`docker stats`            # live container resource usage
`docker top <id>`         # display running processes in a container


## Creation of multiple containers
```bash
for i in {1..5}; do docker run -d -p 80 hello-world; done
docker ps -a
```
The hello-world containers exit immediately after running, so they're already stopped.

## Learn volume mounts and ports

Most real apps need filesystem access and networking.

**Port mapping**
```bash
# Map container port 3000 to host port 3000
docker run -p 3000:3000 node

# Map container port 80 to host port 8080
#   -d: detach terminal
#   8080: port on local host
#   80: port in the container
docker run -d -p 8080:80 nginx

# Map to a random host port
docker run -d -p 80 nginx

# Map multiple ports
docker run -d -p 80:80 -p 443:443 nginx

# Bind to specific network interface
docker run -d -p 127.0.0.1:8080:80 nginx
```

**Volume mount**

```bash
# Mount current directory to /app in container
# What each part does:
#   docker run - creates and runs a container
#   -v $(pwd):/app - mounts a volume:
#   $(pwd) - your current working directory on the host
#   :/app - mapped to /app inside the container
#   ubuntu - the image to use
#   ls /app - command executed inside the container
docker run -v $(pwd):/app ubuntu ls /app

# Mount with read-only access
docker run -v $(pwd):/app:ro ubuntu ls /app

# Named volume (persisted data)
docker run -d -v mydata:/var/lib/mysql mysql

# Windows path example
docker run -v C:\myapp:/app ubuntu ls /app
```

**Volume management commands:**

Named volumes are managed by Docker and persist independently of containers. <br>
**Why use volumes:**
- **Persist data** beyond container lifecycle (databases, uploads, logs)
- **Share data** between containers
- **Avoid rebuilds** during development by mounting source code
- **Better performance** than bind mounts on Windows/Mac
Use these commands to create, inspect, and clean up volumes:

```bash
docker volume create myvolume       # create a named volume
docker volume ls                    # list all volumes
docker volume inspect myvolume      # inspect volume details (location, driver, mount point)
docker volume rm myvolume           # remove a volume (only works if not in use)
docker volume prune                 # remove all unused volumes (frees disk space)
```

**Note** <br>
Volumes can only be removed when no containers (running or stopped) are using them:<br>
step1: Find which containers are using the volume
```bash
docker ps -a --filter volume=myvolume
```
step2: Stop the container(s)
```bash
docker stop <container_id>
```
step3: Remove the container(s)
```bash
docker rm <container_id>
```

step4: Now remove the volume
```bash
docker volume rm myvolume
```

Another alternative way do do it:
```bash
# See which containers use the volume
docker volume inspect myvolume

# Force remove running container
docker rm -f <container_id>

# Then remove volume
docker volume rm myvolume
```

## Check if a docker image is available in official Docker Hub:
```bash
# Search for an image
docker search nginx

# Search with filter for official images
docker search --filter is-official=true alpine
docker search --filter is-official=true nginx
docker search --filter is-official=true python
docker search --filter is-official=true redis

# Limit results
docker search --limit 5 nginx
```

Check if you can pull it:
```bash
# Pull specific tag 
#    docker pull - command to download an image
#    node - official Node.js image name
#    :18-alpine - tag specifying Node.js version 18 with Alpine Linux base
docker pull node:18          # Full Debian-based
docker pull node:18-slim     # Debian (minimal)
docker pull node:18-alpine   # Alpine Linux
docker pull node:latest      # Latest version
docker pull nginx:latest     #
docker pull nginx:alpine     # Nginx on Alpine
docker pull python:3.11-slim # Python slim variant

# verify the OS release:
docker run --rm node:18 cat /etc/os-release
```


## Build your first Dockerfile

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
# Build the image
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

**Advanced Docker build commands:**
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

## Security & hygiene best practices (early!)

Don’t skip these:

- Use official or minimal base images
- Prefer *-slim or distroless
- Avoid running as root inside containers
- Clean unused resources periodically: `docker system prune`

**Cleanup commands:**
```bash
# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune

# Remove all unused volumes
docker volume prune

# Remove all unused networks
docker network prune

# Remove everything unused (containers, images, networks, volumes)
docker system prune -a

# Show disk usage
docker system df
```

## Docker networking basics

```bash
# List networks
docker network ls

# Create a custom network
docker network create mynetwork

# Run containers on the same network
docker run -d --name app1 --network mynetwork nginx
docker run -d --name app2 --network mynetwork alpine

# Inspect network
docker network inspect mynetwork

# Connect a running container to a network
docker network connect mynetwork container_name

# Disconnect from network
docker network disconnect mynetwork container_name

# Remove network
docker network rm mynetwork
```

## Useful debugging commands

```bash
# Copy files from container to host
docker cp container_id:/path/to/file.txt ./local/path/

# Copy files from host to container
docker cp ./local/file.txt container_id:/path/in/container/

# View container resource usage in real-time
docker stats

# View detailed container configuration
docker inspect container_id

# View container processes
docker top container_id

# View container file system changes
docker diff container_id

# Export container as tar archive
docker export container_id > container.tar

# Save image as tar archive
docker save myapp:latest > myapp.tar

# Load image from tar archive
docker load < myapp.tar

# Check container health
docker inspect --format='{{.State.Health.Status}}' container_id
```


**Testing a quick image:**
```bash
# Pull and run in one command
docker run -d -p 80:80 --name webserver nginx

# Test
curl http://localhost

# Clean up
docker stop webserver && docker rm webserver
```

**Working with registries:**
```bash
# Login to Docker Hub
docker login

# Login to Azure Container Registry
docker login myregistry.azurecr.io

# Tag image for registry
docker tag myapp:latest myregistry.azurecr.io/myapp:v1

# Push to registry
docker push myregistry.azurecr.io/myapp:v1

# Pull from private registry
docker pull myregistry.azurecr.io/myapp:v1

# Logout
docker logout
```

---

## Next steps

1. [Custom Site with Nginx and Docker](custom-site-nginx-docker.md)
1. [Docker Compose](compose.md)
