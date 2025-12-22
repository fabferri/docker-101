# Docker: how to start

## Table of Contents

- [Verify the installation](#verify-the-installation)
- [Understand the Docker components](#understand-the-docker-components)
- [Create a Docker group (Linux only)](#create-a-docker-group-linux-only)
- [Useful Docker commands](#useful-docker-commands)
- [Pull a Docker image from Docker Hub](#pull-a-docker-image-from-docker-hub)
- [Running containers interactively](#running-containers-interactively)
- [Running nginx container in background](#running-nginx-container-in-background)
- [Running multiple nginx containers in background](#running-multiple-nginx-containers-in-background)
- [Running redis container in background](#running-redis-container-in-background)
- [Running mongoDB container in background](#running-mongodb-container-in-background)
- [Learn port mappings](#learn-port-mappings)
- [Check docker images in official Docker Hub registry](#check-docker-images-in-official-docker-hub-registry)
- [Build Dockerfile](#build-dockerfile)
- [Advanced Docker build commands](#advanced-docker-build-commands)
- [Cleanup commands](#cleanup-commands)
- [Useful debugging commands](#useful-debugging-commands)
- [hygiene best practices](#hygiene-best-practices)

---

## Verify the installation

Confirm Docker is installed and running.

```bash
docker --version # confirms CLI installation
docker version   # shows the version of docker client and docker server 
docker info      # confirms the Docker daemon is running
```

Some useful commands:

```bash
systemctl show docker         # displays all properties and configuration details of the Docker service (managed by systemd)
systemctl status docker       # Human-readable status summary
systemctl is-active docker    # Just shows "active" or "inactive"
systemctl is-enabled docker   # Check if starts at boot
systemctl show docker --property=MainPID   # Show specific property
systemctl show docker --property=MemoryCurrent  # Memory usage
systemctl show docker --property=ActiveState    # Just the state

# Service management
systemctl start docker          # starts the Docker daemon service on Linux systems using systemd.
systemctl stop docker           # stop the Docker daemon service on Linux systems using systemd.
systemctl restart docker        # restart the Docker daemon service on Linux systems using systemd.
systemctl enable docker         # Enable at boot
systemctl disable docker        # Disable at boot
```

## Understand the Docker components

Before going further, make sure these concepts are clear:

- Image – immutable template (e.g. nginx, python:3.11)
- Container – running (or stopped) instance of an image
- Dockerfile – recipe to build images
- Registry – where images live (Docker Hub, ACR, ECR, etc.)

**Run a test container (sanity check)**

```bash
docker run hello-world
```
Initally docker image is not available locally. Docker pulls the image from the Docker Hub, creates the container, and executes it — successful execution indicates a healthy environment.

```bash
docker images  # show the image "hello-world:latest" automatically dowloaded from the Docker Hub registry
```

## Create a Docker group (Linux only)

- The docker daemon binds to a Unix socket instead of a TCP port. By default that Unix socket (/var/run/docker.sock) is owned by the user root and other users can access it with sudo. For this reason, docker daemon always runs as the root user.
- To avoid having to use sudo when you use the docker command, create a Unix group called docker and add users to it. When the docker daemon starts, it makes the ownership of the Unix socket read/writable by the docker group.

> [!NOTE]
>
> Adding a user to the docker group is equivalent to granting root access, since they can run containers with full host access.
>

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Useful Docker commands

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

## Pull a Docker image from Docker Hub

Try pulling few images for your work from Docker Hub:

```bash
docker pull nginx         # download nginx docker image
docker pull python:3.11   # download linux with python installed

docker images             # list images stored locally
```


## Running containers interactively

Run a container interactively:
```bash
docker run -it ubuntu bash
```
To exit from the container just run `exit` or `CTRL+D` <br>
The same command with specify the bash path: `docker run -it ubuntu /bin/bash`

**More interactive examples:**
```bash
# Run Python interpreter interactively. exit() or Ctrl-D to exit
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

## Running nginx container in background

Running nginx web server in background:
```bash
docker run -d nginx

# Check it's running
docker ps
```

Running nginx in background with port mapping:
```bash
# This command runs an Nginx web server in a Docker container:
#   docker run - creates and starts a new container
#   -d - detached mode (runs in background, doesn't block your terminal)
#   -p 8080:80 - port mapping:
#   8080 = port on your host machine
#   80 = port inside the container (Nginx default HTTP port)
#   Traffic to localhost:8080 gets forwarded to port 80 in the container
#   nginx - the Docker image to use (official Nginx web server in Docker Hub)
docker run -d -p 8080:80 nginx

# Get the container ID or name
# "docker ps" shows ONLY running containers
docker ps   

# To connect to an existing container running in detached mode, use "docker exec"
# Connect to the container with an interactive bash 
# NOTE: 
#    the hostname inside the container is equal to the <container_id>
#    interactive connection to the container accepts the <container_name> as alternative to <container_id>
docker exec -it <container_id> bash

# Test it
# Connect to the ngix container in the host running docker (NOT inside the container!)
curl 127.0.0.1:8080

# Connect to the ngix container in the host
curl <IP_ADDRESS_HOST>:8080

# Stop the container
docker stop <container_id>

# check the container status
docker ps -a
```

The command `docker ps -a` show the STATUS of containers. <br>
`status=exited (0)` means:
  `exited` - the container has stopped running
  `(0)` - the exit code, where 0 means success (the process completed normally without errors)


You can use the <container_name> instead of <container_id>: 
```bash
# Get only container names (running containers)
docker ps --format "{{.Names}}"

docker exec -it <container_name> bash
```

Running nginx in background with a name:
```bash
# Run in background with custom name: 'my-nginx'
docker run -d --name my-nginx -p 8080:80 nginx

# Now you can use the name instead of ID
docker logs my-nginx     # Shows logs and then exits immediately
docker logs -f my-nginx  # Follow logs in real-time
docker stop my-nginx     # Stop container
docker start my-nginx    # Start stopped container
docker rm my-nginx       # Remove container
docker rm -f my-nginx    # Force remove running container
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
# --memory="512m" - limits memory to 512 megabytes
#          Container cannot use more than 512MB of RAM
#          If exceeded, container may be killed or throttled
# --cpus="1.0" - limits CPU usage to 1.0 CPU core
#          Container can use up to 100% of one CPU core
#          With 0.5, it would get 50% of one core
#          With 2.0, it could use 2 full cores
docker run -d --memory="512m" --cpus="1.0" nginx

# Limit to 1GB RAM and 2 CPU cores
docker run -d --memory="1g" --cpus="2.0" nginx

# Memory with reservation (soft limit)
docker run -d --memory="1g" --memory-reservation="500m" nginx

# Check resource usage
docker stats

# Inspect resource limits
docker inspect <container_id> | grep -i memory
docker inspect <container_id> | grep -i cpu
```

## Running multiple nginx containers in background
```bash
# Create multiple nginx containers with different port mappings
# Each container will map to a different host port: 8080, 8081, 8082, 8083, 8084
for i in {0..4}; do 
  docker run -d --name nginx-$i -p $((8080 + i)):80 nginx
done

# Check all containers are running
docker ps

# Test each container in the host
curl http://localhost:8080
curl http://localhost:8081
curl http://localhost:8082
curl http://localhost:8083
curl http://localhost:8084

# Stop all nginx containers
for i in {0..4}; do docker stop nginx-$i; done

# Remove all nginx containers
for i in {0..4}; do docker rm nginx-$i; done
```

Alternative with random port mapping:
```bash
# Create 5 containers with random host ports
for i in {1..5}; do 
  docker run -d --name nginx-random-$i -p 80 nginx
done

# Check assigned ports
docker ps --format "table {{.Names}}\t{{.Ports}}"

# Find specific port for a container
docker port nginx-random-1

# Lists all container IDs (both running and stopped) in quiet mode.
#   docker ps - lists containers
#          -a - all containers (running + stopped)
#          -q - quiet mode (only shows container IDs, no other details)
docker ps -aq 

# Force remove all containers (running or stopped)
docker rm -f $(docker ps -aq)
```

## Running redis container in background 
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

## Running mongoDB container in background 
Running mongoDB in background container with root credentials:
```bash
# 
# Run MongoDB with environment variables
#   docker run -d - runs container in detached mode (background)
#   --name mongodb - names the container "mongodb"
#   -e MONGO_INITDB_ROOT_USERNAME=admin -  sets environment variable to create admin user with username "admin"
#   -e MONGO_INITDB_ROOT_PASSWORD=password - sets environment variable to create admin user with password "password123"
#   mongo - the official MongoDB image from Docker Hub
# NOTE: before running the command are required environment variables for initializing MongoDB with root credentials.
# NOTE: MongoDB listens on default port 27017 inside the container
docker run -d --name mongodb -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=password123 mongo

# Connect to MongoDB shell
docker exec -it mongodb mongosh -u admin -p password123
```

Few mongoDB shell commands:
```console
db.getUsers()          // List users
db.serverStatus()      // Server status     
db.stats()             // Database statistics
db.version()           // MongoDB version
db.hostInfo()          // Host information
db.currentOp()         // Current operations
db.adminCommand({listDatabases: 1})  // Admin command
```

At this point a mongoDB container is running.

```bash
# Execute command directly in the mogoDB container
docker exec -it mongodb mongosh -u admin -p password123 --eval "db.version()"
docker exec -it mongodb mongosh -u admin -p password123 --eval "db.currentOp()"
```

### Create a mongoDB database and insert data manually

```bash
# Connect to MongoDB shell
docker exec -it mongodb mongosh -u admin -p password123

# Inside mongosh:
use mystore                    // Creates/switches to database 

// Create collection and insert documents
db.products.insertMany([
  {name: "Laptop", price: 999, category: "Electronics", stock: 50},
  {name: "Mouse", price: 25, category: "Electronics", stock: 200},
  {name: "Desk", price: 299, category: "Furniture", stock: 30},
  {name: "Chair", price: 150, category: "Furniture", stock: 75}
])

// Verify the data
db.products.find().pretty()
show collections
db.products.countDocuments()
```

### Load data in a mongoDB database from a JSON file
Create a file **products.json** on your host:
```json
[
  {"name": "Laptop_top", "price": 1000, "category": "Electronics", "stock": 50},
  {"name": "Mouse_game", "price": 25, "category": "Electronics", "stock": 200},
  {"name": "mobileDesk", "price": 315, "category": "Furniture", "stock": 30},
  {"name": "WoodChair", "price": 250, "category": "Furniture", "stock": 75}
]
```

Import the JSON file:
```bash
# Copy file to container
docker cp products.json mongodb:/tmp/products.json

# Import using mongoimport
docker exec -it mongodb mongoimport \
  -u admin \
  -p password123 \
  --authenticationDatabase admin \
  --db mystore \
  --collection products \
  --file /tmp/products.json \
  --jsonArray

# Verify
docker exec -it mongodb mongosh -u admin -p password123 --authenticationDatabase admin mystore --eval "db.products.find()"

# Find with filter
docker exec -it mongodb mongosh -u admin -p password123 --authenticationDatabase admin mystore --eval "db.products.find({category: 'Electronics'}).toArray()"

# Show all collections
docker exec -it mongodb mongosh -u admin -p password123 --authenticationDatabase admin mystore --eval "db.getCollectionNames()"
```

Query the data in mongoDB shell:
```bash
docker exec -it mongodb mongosh -u admin -p password123

use mystore

// Find all products
db.products.find()

// Find products in Electronics category
db.products.find({category: "Electronics"})

// Find products under $100
db.products.find({price: {$lt: 100}})

// Count products by category
db.products.countDocuments({category: "Electronics"})

// Update stock
db.products.updateOne({name: "Mouse"}, {$set: {stock: 180}})
```



## Learn port mappings

Most real apps need filesystem access and networking.


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

You cannot remove or change port mappings from an existing container. Port mappings are set when the container is created and are immutable. Port mapping are locked in at container creation and cannot be modified afterward, whether the container is running or stopped. Container needs to be deleted and recreated with different port mapping:
```bash
# Find nginx container ID
docker ps -a --filter ancestor=nginx  

# Remove the old container first
docker rm -f <container_id>

# recreate a new container with different port mapping
docker run -d -p 9090:80 nginx
```

## Check docker images in official Docker Hub registry

```bash
# Search for an image
docker search nginx

# Search with filter for official images
docker search --filter is-official=true alpine
docker search --filter is-official=true nginx
docker search --filter is-official=true python
docker search --filter is-official=true redis

# Limit results
#   docker search - searches Docker Hub registry for images
#   --limit 5 - restricts output to only 5 results (default is 25)
#   nginx - the search term
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
#   docker run - creates and starts a new container
#   --rm       - automatically removes the container after it exits (cleanup, no leftover stopped containers)
#   node:18    - the Node.js version 18 image from Docker Hub
#   cat /etc/os-release - command executed inside the container that displays OS information (distribution name, version)
docker run --rm node:18 cat /etc/os-release
```




## Build Dockerfile

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

## Cleanup commands

```bash
# Remove all stopped containers
docker container prune

# Remove containers and skip confirmation prompt
docker container prune -f

# Remove containers stopped more than 24 hours ago
docker container prune --filter "until=24h"

# Remove all unused images. Removes ONLY images
docker image prune

# Remove ALL unused images (including tagged ones not used by containers)
docker image prune -a

# Remove all unused volumes
docker volume prune

# Remove all unused networks
docker network prune

# Remove everything unused (containers, images, networks, volumes)
# Remove:
# - All stopped containers
# - All networks not used by at least one container
# - All images without at least one container associated to them (not just dangling ones)
# - All build cache
# BUT it preserves all volumes (even unused ones)
docker system prune -a

# System prune including volumes
# Removes everything above PLUS: All unused volumes (volumes not attached to any containers)
docker system prune -a --volumes

# Show disk usage
docker system df
```

Remove everything including running containers:
```bash
# Stop all running containers first
docker stop $(docker ps -q)

# Then remove everything
docker system prune -a --volumes

# Or force remove all containers (running or stopped)
docker rm -f $(docker ps -aq)

# Then clean up images and volumes
docker system prune -a --volumes
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

## hygiene best practices

- Use official or minimal base images
- Prefer *-slim or distroless
- Avoid running as root inside containers
- Clean unused resources periodically: `docker system prune`

---
## Next step

[Docker Volume mount](docker-volume-mount.md)

## Coming back

[Docker 101: first hands-on](README.md)