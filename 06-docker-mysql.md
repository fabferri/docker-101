# Deploying MySQL in Docker

## Directory Structure
Create this structure in your project folder:

MySQL Dockerfile with custom configuration:

```console
my-mysql-project/
├── Dockerfile
├── my.cnf              # MySQL configuration
└── init.sql            # Database initialization script
```

## step1: Create my.cnf (MySQL Configuration)

- MySQL loads all .cnf files from /etc/mysql/conf.d/ at startup
- Settings override defaults from /etc/mysql/my.cnf
- Applied every time the container starts
This file customizes MySQL server settings: 

```bash
# my.cnf
[mysqld]
# Performance tuning
max_connections=200
max_allowed_packet=64M

# Character set
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci

# Logging
general_log=0
slow_query_log=1
slow_query_log_file=/var/log/mysql/slow-query.log
long_query_time=2

# InnoDB settings
innodb_buffer_pool_size=1G
innodb_log_file_size=256M

[client]
default-character-set=utf8mb4
```

## step2: Create **init.sql** (Initialization Script)

- This script runs only on first container startup (when database is empty)
- MySQL runs scripts in /docker-entrypoint-initdb.d/ <ins>only once</ins>
- Only executes when **/var/lib/mysql** is empty (first run)
- Scripts run in <ins>alphabetical order</ins>
- Runs after MySQL is fully started


```sql
-- init.sql
-- Create tables
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial data
INSERT INTO users (username, email) VALUES 
    ('admin', 'admin@example.com'),
    ('user1', 'user1@example.com');

INSERT INTO products (name, price) VALUES 
    ('Product 1', 19.99),
    ('Product 2', 29.99);

-- Create additional user
CREATE USER IF NOT EXISTS 'readonly'@'%' IDENTIFIED BY 'readonlypass';
GRANT SELECT ON myapp.* TO 'readonly'@'%';
FLUSH PRIVILEGES;
```

## Step3: Dockerfile

```dockerfile
FROM mysql:8.0

# Environment variables
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=myapp
ENV MYSQL_USER=appuser
ENV MYSQL_PASSWORD=apppassword


# Copy custom MySQL configuration to /etc/mysql/conf.d/
# MySQL automatically loads all .cnf files from this directory
COPY my.cnf /etc/mysql/conf.d/

# Copy initialization scripts (run on first startup)
# Copy initialization scripts to /docker-entrypoint-initdb.d/
# MySQL runs all .sql, .sql.gz, and .sh files from this directory on first startup
COPY init.sql /docker-entrypoint-initdb.d/

# Set timezone
ENV TZ=UTC

EXPOSE 3306

# Data persists in /var/lib/mysql (use volume)
VOLUME /var/lib/mysql
```

## step4: Build and Run

```bash
# Build the image
docker build -t my-mysql .

# Run the container with named volume for data persistence
docker run -d \
  --name mysql-db \
  -p 3306:3306 \
  -v mysql-data:/var/lib/mysql \
  my-mysql

# OR run with environment variables (override Dockerfile values)
docker run -d \
  --name mysql-db \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=newsecurepassword \
  -e MYSQL_DATABASE=productiondb \
  -v mysql-data:/var/lib/mysql \
  my-mysql

# Check logs to see initialization
docker logs mysql-db

# Connect to MySQL
docker exec -it mysql-db mysql -u root -p
# Password: rootpassword

# Test the initialized data
docker exec -it mysql-db mysql -u appuser -papppassword myapp -e "SELECT * FROM users;"

# View logs
docker logs mysql-db
```

## Dockerfile with healthcheck

Best practices:

- Never hardcode passwords in production - use Docker secrets or environment variables
- Always use named volumes for /var/lib/mysql to persist data
- Use healthcheck to monitor MySQL status
- Limit resources with --memory and --cpus flags

Production-ready Dockerfile with healthcheck:
```dockerfile
FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
ENV MYSQL_DATABASE=${MYSQL_DATABASE}

COPY my.cnf /etc/mysql/conf.d/
COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD mysqladmin ping -h localhost -u root -p${MYSQL_ROOT_PASSWORD} || exit 1

VOLUME /var/lib/mysql
```

Run with build args (secure):
```bash
docker build \
  --build-arg MYSQL_ROOT_PASSWORD=securepass \
  --build-arg MYSQL_DATABASE=mydb \
  -t my-mysql .
```

---

## Next step

[Working with registries](07-registries.md)

## Coming back

[Docker 101: first trek](README.md)