# Docker compose: full stack example

## Common Docker workflows

## Step 1: Create a new directory for your project
```bash
mkdir my-app1
cd my-app1
```

## Step 2: Create the docker-compose.yml file
```bash
cat > docker-compose.yml << 'EOF'
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
EOF
```

# Step 3: Verify the docker-compose.yml syntax
```bash
docker compose config
```

# Step 4: Pull the images from docker hub
```bash
docker compose pull
```

# Step 5: Start all services in detached mode (-d runs in background)
```bash
docker compose up -d
```

# Step 6: Verify services are running
```bash
docker compose ps
```

```bash
# 1. Create Dockerfile and docker-compose.yml
# 2. Build and run
docker compose up -d --build

# What the "docker compose up -d --build" does:
# - "docker compose up": Starts all services defined in docker-compose.yml
# - "-d" (detached mode): Runs containers in the background (doesn't block terminal)
# - "--build": Forces rebuild of images before starting containers
#
# This command combines three operations:
# 1. Builds/rebuilds Docker images for services that use "build: ." directive
# 2. Creates containers from the images
# 3. Starts all containers in detached mode
#
# Use cases:
# - First time setup: Builds images and starts services
# - After code changes: Rebuilds images with latest code and restarts
# - After Dockerfile changes: Ensures images include latest build instructions
#
# Without --build: "docker compose up -d" uses existing images (faster, but won't include code changes)
# Without -d: Runs in foreground (blocks terminal, shows logs, stops when you press Ctrl+C)

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

Example of docker compose with web + database + cache:
File: **docker-compose.yml**
```yaml
