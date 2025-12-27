# Ruby on Rails with PostgreSQL in Docker

Guide to containerize a Ruby on Rails application with PostgreSQL database using Docker and Docker Compose.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Configuration Files](#configuration-files)
- [Running the Application](#running-the-application)
- [Common Commands](#common-commands)
- [Database Operations](#database-operations)
- [Development Workflow](#development-workflow)
- [Production Considerations](#production-considerations)
- [Troubleshooting](#troubleshooting)

---

## Overview

This setup provides a fully containerized Ruby on Rails development environment with:

- **Ruby on Rails 7.x** - Web application framework
- **PostgreSQL 16** - Relational database
- **Docker Compose** - Multi-container orchestration
- **Volume mounts** - Live code reloading during development
- **Isolated environment** - No local Ruby or PostgreSQL installation needed

---

## Project Structure

```
rails-postgres-app/
├── app/                    # Rails application code
│   ├── controllers/
│   ├── models/
│   ├── views/
│   └── ...
├── config/                 # Rails configuration
│   ├── database.yml        # Database configuration
│   ├── routes.rb
│   └── ...
├── db/                     # Database files
│   ├── migrate/           # Database migrations
│   └── seeds.rb           # Seed data
├── public/                # Static files
├── Dockerfile             # Rails container definition
├── docker-compose.yml     # Multi-container orchestration
├── .dockerignore          # Files to exclude from Docker
├── Gemfile                # Ruby dependencies
├── Gemfile.lock           # Locked gem versions
└── README.md              # Project documentation
```

---

## Prerequisites

- **Docker** - [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** - 
- **Git** (optional) - For version control

**No Ruby or PostgreSQL installation needed!** Everything runs in containers.

---

## Setup Instructions

### 1. Create a New Rails Application

```bash
# Create project directory
mkdir rails-postgres-app
cd rails-postgres-app

# Create Rails app using Docker (no local Ruby needed)
docker run --rm -v "$PWD":/app -w /app ruby:3.3 \
  bash -c "gem install rails && rails new . --database=postgresql --skip-bundle"
```

### 2. Create Required Files

Create the following files in your project directory:

---

## Configuration Files

### Dockerfile

File: **Dockerfile**

```dockerfile
# Use Ruby 3.3 as base image
FROM ruby:3.3

# Install system dependencies
# - nodejs: JavaScript runtime for Rails asset pipeline
# - postgresql-client: PostgreSQL client libraries
# - build-essential: Compilation tools for native gems
RUN apt-get update -qq && apt-get install -y \
    nodejs \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Gemfile and Gemfile.lock first
# This allows Docker to cache bundle install layer
COPY Gemfile Gemfile.lock ./

# Install Ruby gems
RUN bundle install

# Copy the rest of the application
COPY . .

# Expose port 3000 for the Rails server
EXPOSE 3000

# Precompile assets for production (optional)
# RUN bundle exec rails assets:precompile

# Start Rails server
# -b 0.0.0.0: Bind to all network interfaces (required for Docker)
CMD ["rails", "server", "-b", "0.0.0.0"]
```

---

### Docker Compose Configuration

File: **docker-compose.yml**

```yaml
version: "3.9"

services:
  # PostgreSQL Database Service
  db:
    image: postgres:16
    container_name: rails_postgres_db
    
    # Persist database data
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
    # Database credentials
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp_development
    
    # Expose PostgreSQL port (optional, for external access)
    ports:
      - "5432:5432"
    
    # Health check
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Rails Web Application Service
  web:
    build: .
    container_name: rails_web_app
    
    # Run database setup on startup
    command: bash -c "
      rm -f tmp/pids/server.pid &&
      bundle exec rails db:create db:migrate db:seed &&
      rails server -b 0.0.0.0
      "
    
    # Mount local code for live reloading
    volumes:
      - .:/app
      - bundle_cache:/usr/local/bundle
    
    # Expose Rails port
    ports:
      - "3000:3000"
    
    # Database connection settings
    environment:
      DATABASE_HOST: db
      DATABASE_USER: postgres
      DATABASE_PASSWORD: password
      RAILS_ENV: development
    
    # Wait for database to be ready
    depends_on:
      db:
        condition: service_healthy

# Named volumes for data persistence
volumes:
  postgres_data:    # Database files
  bundle_cache:     # Cached gems
```

---

### Database Configuration

File: **config/database.yml**

```yaml
default: &default
  adapter: postgresql
  encoding: unicode
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  host: <%= ENV.fetch("DATABASE_HOST", "localhost") %>
  username: <%= ENV.fetch("DATABASE_USER", "postgres") %>
  password: <%= ENV.fetch("DATABASE_PASSWORD", "password") %>

development:
  <<: *default
  database: myapp_development

test:
  <<: *default
  database: myapp_test

production:
  <<: *default
  database: myapp_production
  username: myapp
  password: <%= ENV["MYAPP_DATABASE_PASSWORD"] %>
```

---

### Gemfile

File: **Gemfile**

```ruby
source "https://rubygems.org"

# Ruby version
ruby "3.3.0"

# Rails framework
gem "rails", "~> 7.1"

# PostgreSQL adapter
gem "pg", "~> 1.5"

# Web server
gem "puma", ">= 5.0"

# Asset pipeline
gem "sprockets-rails"

# JavaScript bundling
gem "jsbundling-rails"

# Hotwire's SPA-like page accelerator
gem "turbo-rails"

# Hotwire's modest JavaScript framework
gem "stimulus-rails"

# Build JSON APIs
gem "jbuilder"

# Windows timezone data
gem "tzinfo-data", platforms: %i[ windows jruby ]

# Reduces boot times through caching
gem "bootsnap", require: false

group :development, :test do
  # Debugging
  gem "debug", platforms: %i[ mri windows ]
  
  # Testing framework
  gem "rspec-rails"
end

group :development do
  # Use console on exceptions pages
  gem "web-console"
end
```

---

### Docker Ignore File

File: **.dockerignore**

```
# Git files
.git
.gitignore

# Logs
log/*
*.log

# Temporary files
tmp/*
!tmp/.keep

# Node modules
node_modules/
yarn-error.log

# Environment files
.env
.env.*

# Database files
*.sqlite3
*.sqlite3-journal

# Cache
.cache/
public/assets/
public/packs/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Bundler
vendor/bundle/
.bundle/
```

---

## Running the Application

### First Time Setup

```bash
# Build and start containers
docker compose up --build

# The application will:
# 1. Build the Rails image
# 2. Start PostgreSQL database
# 3. Create database
# 4. Run migrations
# 5. Seed database
# 6. Start Rails server

# Access the application at: http://localhost:3000
```

### Subsequent Starts

```bash
# Start containers (no rebuild needed)
docker compose up

# Or run in background
docker compose up -d

# View logs
docker compose logs -f web
```

### Stop the Application

```bash
# Stop containers (preserves data)
docker compose down

# Stop and remove volumes (deletes data)
docker compose down -v
```

---

## Common Commands

### Container Management

```bash
# Start services in background
docker compose up -d

# Stop services
docker compose down

# Restart services
docker compose restart

# View running containers
docker compose ps

# View logs
docker compose logs -f        # All services
docker compose logs -f web    # Rails app only
docker compose logs -f db     # Database only
```

### Rails Commands

```bash
# Run Rails console
docker compose exec web rails console

# Run Rails generator
docker compose exec web rails generate model User name:string email:string

# Check routes
docker compose exec web rails routes

# Run tests
docker compose exec web bundle exec rspec

# Access bash shell
docker compose exec web bash
```

### Bundle Management

```bash
# Install new gem
# 1. Add gem to Gemfile
# 2. Run bundle install
docker compose exec web bundle install

# Update gems
docker compose exec web bundle update
```

---

## Database Operations

### Migrations

```bash
# Create a new migration
docker compose exec web rails generate migration AddAgeToUsers age:integer

# Run pending migrations
docker compose exec web rails db:migrate

# Rollback last migration
docker compose exec web rails db:rollback

# Reset database
docker compose exec web rails db:reset

# Drop, create, migrate, and seed
docker compose exec web rails db:setup
```

### Database Access

```bash
# Rails database console
docker compose exec web rails dbconsole

# PostgreSQL psql client
docker compose exec db psql -U postgres -d myapp_development

# Backup database
docker compose exec db pg_dump -U postgres myapp_development > backup.sql

# Restore database
docker compose exec -T db psql -U postgres -d myapp_development < backup.sql
```

### Seed Data

File: **db/seeds.rb**

```ruby
# Create sample users
User.create([
  { name: "Alice Johnson", email: "alice@example.com" },
  { name: "Bob Smith", email: "bob@example.com" },
  { name: "Charlie Brown", email: "charlie@example.com" }
])

puts "Created #{User.count} users"
```

Run seeds:
```bash
docker compose exec web rails db:seed
```

---

## Development Workflow

### 1. Make Code Changes
Edit files locally - changes appear instantly in the container due to volume mounts.

### 2. Add New Gem
```bash
# Edit Gemfile, then:
docker compose exec web bundle install

# Restart if needed
docker compose restart web
```

### 3. Create New Feature
```bash
# Generate scaffold
docker compose exec web rails generate scaffold Post title:string body:text

# Run migration
docker compose exec web rails db:migrate

# Access at: http://localhost:3000/posts
```

### 4. View Logs
```bash
# Real-time logs
docker compose logs -f web
```

---

## Production Considerations

### Optimized Production Dockerfile

File: **Dockerfile.production**

```dockerfile
FROM ruby:3.3-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    nodejs \
    yarn

WORKDIR /app

# Install gems
COPY Gemfile Gemfile.lock ./
RUN bundle config set --local deployment 'true' && \
    bundle config set --local without 'development test' && \
    bundle install --jobs=4 --retry=3

# Copy application
COPY . .

# Precompile assets
RUN SECRET_KEY_BASE=dummy bundle exec rails assets:precompile

# Runtime stage
FROM ruby:3.3-alpine

RUN apk add --no-cache \
    postgresql-client \
    nodejs \
    tzdata

WORKDIR /app

# Copy built artifacts
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /app /app

# Create non-root user
RUN adduser -D appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 3000

CMD ["bundle", "exec", "puma", "-C", "config/puma.rb"]
```

### Production Environment Variables

```bash
# Use .env file or set environment variables
RAILS_ENV=production
SECRET_KEY_BASE=your_secret_key_here
DATABASE_URL=postgresql://user:password@host:5432/database
RAILS_SERVE_STATIC_FILES=true
RAILS_LOG_TO_STDOUT=true
```

### Build for Production

```bash
# Build production image
docker build -f Dockerfile.production -t rails-app:production .

# Run with environment variables
docker run -p 3000:3000 \
  -e RAILS_ENV=production \
  -e SECRET_KEY_BASE=your_secret_key \
  -e DATABASE_URL=postgresql://... \
  rails-app:production
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 3000
lsof -ti:3000 | xargs kill -9

# Or change port in docker-compose.yml
ports:
  - "3001:3000"  # Use port 3001 instead
```

### Database Connection Errors

```bash
# Check database is running
docker compose ps

# Check database logs
docker compose logs db

# Restart database
docker compose restart db

# Recreate database
docker compose exec web rails db:drop db:create db:migrate
```

### Permission Errors

```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Or run as root (not recommended)
docker compose exec --user root web bash
```

### Container Won't Start

```bash
# Check logs
docker compose logs web

# Remove old containers and volumes
docker compose down -v

# Rebuild from scratch
docker compose up --build --force-recreate
```

### Bundle Install Failures

```bash
# Clear bundle cache
docker compose down -v
docker volume rm rails-postgres-app_bundle_cache

# Rebuild
docker compose up --build
```

### Migrations Won't Run

```bash
# Check migration status
docker compose exec web rails db:migrate:status

# Force migration version
docker compose exec web rails db:migrate:up VERSION=20231225120000

# Reset database (WARNING: deletes all data)
docker compose exec web rails db:reset
```

---

## Quick Reference

### Essential Commands Cheat Sheet

```bash
# Start everything
docker compose up -d

# Stop everything
docker compose down

# Rebuild after Gemfile changes
docker compose up --build

# Rails console
docker compose exec web rails console

# Database console
docker compose exec web rails dbconsole

# Run migrations
docker compose exec web rails db:migrate

# View logs
docker compose logs -f web

# Bash shell
docker compose exec web bash

# Clean up (removes all data!)
docker compose down -v
```

---

## Additional Resources

- [Rails Guides](https://guides.rubyonrails.org/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

---

## Best Practices

1. **Use volume mounts** for development (live code reloading)
2. **Use .dockerignore** to exclude unnecessary files
3. **Pin versions** in Gemfile for reproducibility
4. **Use health checks** in docker-compose.yml
5. **Separate development and production** Dockerfiles
6. **Use environment variables** for configuration
7. **Don't commit secrets** to version control
8. **Use named volumes** for data persistence
9. **Run as non-root user** in production
10. **Keep images small** using alpine or multi-stage builds

---

