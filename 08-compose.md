# Docker compose

## Table of Contents

- [Install Docker Compose](#install-docker-compose)
- [Check your Docker Compose version](#check-your-docker-compose-version)
- [Docker Compose file format version](#docker-compose-file-format-version)
- [Step-by-step deployment of the basic example](#step-by-step-deployment-of-the-basic-example)
- [Full stack example](#full-stack-example)
- [Docker Compose commands](#docker-compose-commands)
- [Configure your workflow](#configure-your-workflow)
- [Common Docker workflows](#common-docker-workflows)

---

Docker Compose lets you define and run multi‑container Docker applications using a single **docker-compose.yml**. <br>

Compose is essential for:

- Multi-container apps
- Local dev environments
- Repeatable setups



## Install Docker Compose

```bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
docker compose version
```

## Check your Docker Compose version

```bash
docker compose version
```

## Docker Compose file format version

The `version` field in <ins>**docker-compose.yml**</ins> specifies the **Compose file format version**.

```yaml
version: '3.8'  # Compose file format version (NOT Docker or Docker Compose version)
```

version: '3.8' 
- requires Docker Engine 19.03.0+
- determines which **features and syntax** (networks, volumes, build args, etc.) are available in the YAML file
- **Important:** As of Docker Compose V2 (2020+), the `version` field is **optional** and can be omitted. The latest features are automatically available.

```yaml
# Modern approach - version field is optional
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

## Step-by-step deployment of the basic example

```bash
# Step 1: Create a new directory for your project
mkdir my-docker-app
cd my-docker-app

# Step 2: Create the docker-compose.yml file
cat > docker-compose.yml << 'EOF'
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
EOF

# Step 3: Verify the docker-compose.yml syntax
docker compose config

# Step 4: Pull the images (optional, but good to verify)
docker compose pull

# Step 5: Start all services in detached mode (-d runs in background)
docker compose up -d

# Step 6: Verify services are running
docker compose ps
# You should see:
# - web service running on port 8080
# - db service running (no exposed ports, internal only)

# Step 7: Check the logs
docker compose logs
# Or follow logs in real-time:
docker compose logs -f

# Step 8: Test the web service
# Open browser to http://localhost:8080
# Or use curl:
curl http://localhost:8080

# Step 9: Access the database (if needed)
docker compose exec db psql -U postgres
# Type \q to exit psql

# Additional PostgreSQL commands for verification:

# Check PostgreSQL version
docker compose exec db psql -U postgres -c "SELECT version();"

# List all databases
docker compose exec db psql -U postgres -c "\l"

# Connect to a specific database
docker compose exec db psql -U postgres -d postgres

# Check database connection info
docker compose exec db psql -U postgres -c "\conninfo"

# List all tables in current database
docker compose exec db psql -U postgres -c "\dt"
# Note: "Did not find any relations" means no tables exist yet - this is normal for a fresh database

# Create a sample table to test
docker compose exec db psql -U postgres -c "CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(100), email VARCHAR(100));"

# Now list tables again - you should see the 'users' table
docker compose exec db psql -U postgres -c "\dt"

# Insert sample data
docker compose exec db psql -U postgres -c "INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');"

# Query the data
docker compose exec db psql -U postgres -c "SELECT * FROM users;"

# Describe table structure
docker compose exec db psql -U postgres -c "\d users"

# Drop the test table when done
docker compose exec db psql -U postgres -c "DROP TABLE users;"

# Check PostgreSQL is accepting connections
docker compose exec db pg_isready -U postgres

# View PostgreSQL logs
docker compose logs db
docker compose logs -f db  # Follow logs in real-time

# Check PostgreSQL process status
docker compose exec db ps aux

# View PostgreSQL configuration
docker compose exec db cat /var/lib/postgresql/data/postgresql.conf

# Create a test database
docker compose exec db psql -U postgres -c "CREATE DATABASE testdb;"

# List all users/roles
docker compose exec db psql -U postgres -c "\du"

# Check disk space used by PostgreSQL
docker compose exec db df -h /var/lib/postgresql/data

# Step 10: View resource usage
docker compose top

# Step 11: When done, stop the services
docker compose stop

# Step 12: Remove containers (keeps volumes/data)
docker compose down

# check the volume
docker volume ls

# Step 13: Remove everything including volumes (DELETES DATA!)
docker compose down -v
```

**What happens during deployment:**

1. **Docker Compose reads** the YAML file
2. **Creates a network** for the services to communicate
3. **Pulls images** if not already available locally:
   - `nginx:latest`
   - `postgres:15`
4. **Creates a named volume** `db-data` for persistent PostgreSQL data
5. **Starts containers**:
   - `web` container from nginx image, mapping port 8080→80
   - `db` container from postgres:15 image with password set
6. **Attaches volume** to db container at `/var/lib/postgresql/data`

**Service access:**
- **Web server:** http://localhost:8080 (nginx welcome page)
- **Database:** Internal only, accessible from web container via hostname `db` on port 5432
- **Data persistence:** PostgreSQL data stored in `db-data` volume survives container restarts

## Docker Compose commands

```bash
docker compose up -d          # Start all services
docker compose ps             # View running services
docker compose logs           # View logs
docker compose logs -f app    # follow logs for specific service
docker compose stop           # Stop all services
docker compose down           # Stop and remove containers
docker compose down -v        # Remove containers and volumes
docker compose up -d --build  # Rebuild and start
docker compose up -d --scale app=3  # Scale a service
docker compose exec app bash  # Execute command in a service
docker compose top            # View resource usage
```





---

## Coming back

[Docker 101: first trek](README.md)