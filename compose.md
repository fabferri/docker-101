# Docker compose

## Install Docker Compose

```bash
docker compose version
```

Compose is essential for:
- Multi-container apps
- Local dev environments
- Repeatable setups

**Basic docker-compose.yml example:**
```yaml
version: '3.8'
services:
  web:
    image: nginx
    ports:
      - "8080:80"
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: example
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

**Full stack example (web + database + cache):**
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
  
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data
  
  cache:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  postgres-data:
```

**Docker Compose commands:**
```bash
# Start all services
docker compose up -d

# View running services
docker compose ps

# View logs
docker compose logs
docker compose logs -f app      # follow logs for specific service

# Stop all services
docker compose stop

# Stop and remove containers
docker compose down

# Remove containers and volumes
docker compose down -v

# Rebuild and start
docker compose up -d --build

# Scale a service
docker compose up -d --scale app=3

# Execute command in a service
docker compose exec app bash

# View resource usage
docker compose top
```

## Configure your workflow
Depending on your use case:

- Local dev → Docker + volumes + Compose
- CI/CD → non-root builds, small images, multi-stage builds
- Cloud → tag images, push to registry (e.g., Azure Container Registry)

Example tagging:
```bash
docker tag myapp myregistry.azurecr.io/myapp:v1
docker push myregistry.azurecr.io/myapp:v1
```

## Common Docker workflows

**Development workflow:**
```bash
# 1. Create Dockerfile and docker-compose.yml
# 2. Build and run
docker compose up -d --build

# 3. Check logs
docker compose logs -f

# 4. Make code changes (using volumes, no rebuild needed)
# 5. Restart service if needed
docker compose restart app

# 6. Clean up when done
# docker compose down stops all running services defined in your docker-compose.yml and 
# removes the containers and networks that were created. 
# By default, it preserves volumes (persistent data).
docker compose down
```