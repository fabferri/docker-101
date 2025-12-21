# Docker 101: Getting Up and Running with Docker

A comprehensive, step-by-step guide to get you started with Docker, from installation to building and running your own containerized applications.

## Table of Contents
- [1. Verify Docker Installation](#1-verify-docker-installation)
- [2. Understand Docker Components](#2-understand-docker-components)
- [3. Create Docker Group (Linux Only)](#3-create-docker-group-linux-only)
- [4. Pull Real Images](#4-pull-real-images)
- [5. Run and Manage Containers](#5-run-and-manage-containers)
- [6. Create Multiple Containers](#6-create-multiple-containers)
- [7. Learn Volume Mounts and Ports](#7-learn-volume-mounts-and-ports)
- [8. Build Your First Dockerfile](#8-build-your-first-dockerfile)
- [9. Install Docker Compose](#9-install-docker-compose)
- [10. Configure Your Workflow](#10-configure-your-workflow)
- [11. Security & Hygiene Best Practices](#11-security--hygiene-best-practices)
- [Resources](#resources)

---

## 1. Verify Docker Installation

Confirm Docker is installed and running on your system.

```bash
docker --version
docker info
```

**What these commands do:**
- `docker --version` → Confirms CLI installation
- `docker version` → Shows the version of both Docker client and Docker server
- `docker info` → Confirms the Docker daemon is running

### Run a Test Container (Sanity Check)

```bash
docker run hello-world
```

Initially, the Docker image is not available locally and will be pulled from Docker Hub.

**Success means:**
- Docker pulled an image from the registry
- Created a container from that image
- Executed it successfully

If this works, your environment is fundamentally healthy and ready to go!

---

## 2. Understand Docker Components

Before going further, make sure these concepts are clear:

| Component | Description |
|-----------|-------------|
| **Image** | Immutable template (e.g., `nginx`, `python:3.11`) |
| **Container** | Running (or stopped) instance of an image |
| **Dockerfile** | Recipe/instructions to build custom images |
| **Registry** | Where images are stored and shared (Docker Hub, ACR, ECR, etc.) |

**Key Points:**
- Images are read-only templates
- Containers are runtime instances that can be started, stopped, and removed
- Dockerfiles define how to build custom images
- Registries (like Docker Hub) host and distribute images

---

## 3. Create Docker Group (Linux Only)

**Why is this needed?**
- The Docker daemon binds to a Unix socket instead of a TCP port
- By default, that Unix socket is owned by the user `root` and other users can access it with `sudo`
- The Docker daemon always runs as the root user
- To avoid having to use `sudo` when you use the `docker` command, create a Unix group called `docker` and add users to it

**Setup:**

```bash
sudo usermod -aG docker $USER
newgrp docker
```

After running these commands, you can use Docker commands without `sudo`.

---

## 4. Pull Real Images

Try pulling some meaningful images from Docker Hub:

```bash
docker pull nginx
docker pull python:3.11
```

**List all locally stored images:**

```bash
docker images
```

This shows all images you've downloaded, including their repository, tag, image ID, creation date, and size.

---

## 5. Run and Manage Containers

### Run a Container Interactively

```bash
docker run -it ubuntu bash
```

To exit from the container, just run `exit` or press `CTRL+D`.

You can also specify the bash path explicitly:
```bash
docker run -it ubuntu /bin/bash
```

### Run a Container in the Background

```bash
docker run -d -p 8080:80 nginx
```

This runs nginx in detached mode (`-d`) and maps port 8080 on your host to port 80 in the container.

### Useful Container Management Commands

| Command | Description |
|---------|-------------|
| `docker ps` | List running containers |
| `docker ps -a` | List all containers (includes stopped ones) |
| `docker logs <id>` | View logs from a container |
| `docker stop <id>` | Stop a running container |
| `docker rm <id>` | Remove a container |
| `docker images` | List all images stored locally |

---

## 6. Create Multiple Containers

You can easily create multiple containers using a simple loop:

```bash
for i in {1..5}; do docker run -d -p 80 hello-world; done
docker ps -a
```

This creates 5 containers from the `hello-world` image. Use `docker ps -a` to see all of them.

---

## 7. Learn Volume Mounts and Ports

Most real applications need filesystem access and networking capabilities.

### Port Mapping

Map a port from your host machine to a container:

```bash
docker run -p 3000:3000 node
```

The format is `-p HOST_PORT:CONTAINER_PORT`.

### Volume Mount

Mount a directory from your host into a container:

```bash
docker run -v $(pwd):/app ubuntu ls /app
```

This mounts your current directory to `/app` inside the container. **This is how you avoid rebuilding images on every code change** during development.

**Common use cases:**
- Mount source code for live development
- Persist data from databases
- Share configuration files

---

## 8. Build Your First Dockerfile

Create a simple Dockerfile for a Python application:

**Example Dockerfile:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
CMD ["python", "app.py"]
```

**Build and run:**

```bash
docker build -t myapp .
docker run myapp
```

**Dockerfile Instructions Explained:**
- `FROM` - Base image to build upon
- `WORKDIR` - Sets the working directory inside the container
- `COPY` - Copies files from host to container
- `CMD` - Default command to run when container starts

---

## 9. Install Docker Compose

Verify Docker Compose is installed:

```bash
docker compose version
```

**Why use Docker Compose?**

Compose is essential for:
- Multi-container applications
- Local development environments
- Repeatable, reproducible setups

**Example usage:**

```bash
docker compose up -d
```

This starts all services defined in your `docker-compose.yml` file in detached mode.

---

## 10. Configure Your Workflow

Depending on your use case, configure Docker appropriately:

### Local Development
- Use Docker + volumes + Compose
- Enable live code reloading with volume mounts
- Use `docker-compose.yml` for multi-service apps

### CI/CD
- Use non-root builds
- Create small, optimized images
- Implement multi-stage builds

### Cloud Deployment
- Tag images properly
- Push to a container registry (e.g., Azure Container Registry)

**Example tagging and pushing:**

```bash
docker tag myapp myregistry.azurecr.io/myapp:v1
docker push myregistry.azurecr.io/myapp:v1
```

---

## 11. Security & Hygiene Best Practices

**Don't skip these important practices:**

### Use Official and Minimal Base Images
- Prefer official images from trusted sources
- Use `*-slim` or `distroless` variants when possible
- Smaller images = smaller attack surface

### Don't Run as Root
- Avoid running processes as root inside containers
- Create and use non-root users in your Dockerfiles

### Clean Up Regularly
Remove unused resources periodically:

```bash
docker system prune
```

This removes:
- All stopped containers
- All networks not used by at least one container
- All dangling images
- All build cache

**Additional Best Practices:**
- Use specific image tags instead of `latest` in production
- Scan images for vulnerabilities
- Keep Docker and images updated
- Use `.dockerignore` to exclude unnecessary files from builds
- Minimize the number of layers in your images

---

## Resources

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)

---

## License

This is a tutorial repository for educational purposes.
