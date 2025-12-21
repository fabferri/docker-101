# Multi-Container Application with Docker Compose

A demonstration of a multi-container application using Docker Compose with a Flask web application and Redis database.

## Architecture

This application consists of two services:

1. **Web Service** - A Flask (Python) web application
2. **Redis Service** - A Redis database for storing data

The services communicate through a Docker network and share data through volumes.

## What's Inside

- `docker-compose.yml` - Defines and configures both services
- `web/app.py` - Flask web application
- `web/requirements.txt` - Python dependencies
- `web/Dockerfile` - Web service container configuration

## How to Use

### Start all services

```bash
cd multi-container
docker compose up -d
```

This command will:
- Build the web service image
- Pull the Redis image
- Create a network for inter-container communication
- Create a volume for Redis data persistence
- Start both containers in the background

### Access the application

Open your browser and visit: http://localhost:8080

You'll see a page with a visit counter that demonstrates communication between the web app and Redis.

### View logs

```bash
# All services
docker compose logs

# Specific service
docker compose logs web
docker compose logs redis

# Follow logs in real-time
docker compose logs -f
```

### Check service status

```bash
docker compose ps
```

### Stop all services

```bash
docker compose down
```

### Stop and remove volumes (reset data)

```bash
docker compose down -v
```

## Key Concepts Demonstrated

### 1. Service Dependencies
The web service depends on Redis:
```yaml
depends_on:
  - redis
```

### 2. Networking
Services communicate through a custom bridge network:
```yaml
networks:
  - app-network
```

The web service can reach Redis using the hostname `redis`.

### 3. Volume Persistence
Redis data persists across container restarts:
```yaml
volumes:
  - redis-data:/data
```

### 4. Environment Variables
Configuration passed to containers:
```yaml
environment:
  - REDIS_HOST=redis
  - REDIS_PORT=6379
```

### 5. Port Mapping
Services exposed to the host:
```yaml
ports:
  - "8080:5000"  # host:container
```

## Development Workflow

### Rebuild services after code changes

```bash
docker compose up -d --build
```

### Scale services (create multiple instances)

```bash
docker compose up -d --scale web=3
```

### Execute commands in running containers

```bash
docker compose exec web python --version
docker compose exec redis redis-cli ping
```

## Troubleshooting

### Check if containers are running
```bash
docker compose ps
```

### View real-time logs
```bash
docker compose logs -f web
```

### Restart a specific service
```bash
docker compose restart web
```

### Access container shell
```bash
docker compose exec web bash
docker compose exec redis sh
```

## Learning Points

1. **Docker Compose simplifies multi-container apps** - Define everything in one YAML file
2. **Service discovery** - Containers can find each other by service name
3. **Declarative configuration** - Describe desired state, Docker handles the rest
4. **Easy development** - Start/stop entire application stack with one command
5. **Production-ready** - Same compose file works in different environments

## Next Steps

- Try modifying the Flask app and rebuild
- Add another service (e.g., PostgreSQL or MongoDB)
- Experiment with environment variables
- Learn about Docker Compose overrides for different environments
