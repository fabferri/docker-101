#  Ruby on Rails container

Ruby is a high‑level language used to build applications, scripts, and web services.

## Run Ruby without a Dockerfile

In the local host creates a new folder:
```bash
mkdir $(pwd)/app
```

Copy the script the script: [basic ruby script](ruby-basic-script.rb) inside the new folder $(pwd)/app

Create a ruby container in backgroud:
```bash
# docker run - Executes a new container
#   -d - Create the container in background
#   -v "$PWD":/app - Mounts current directory ($PWD) to /app inside container
#   Shares your local files with the container
#   Changes made in container appear in your local directory
#   -w /app - Sets working directory to /app inside the container
#   All commands execute from this directory
#   ruby:3.3 - Uses the official Ruby 3.3 Docker image
#   sleep infinity - Keep container alive with sleep
docker run -d --name myruby -v "$PWD":/app -w /app ruby:3.3 sleep infinity

# Then connect and run your scripts
docker exec -it myruby bash
# inside the container run the ruby script in the folder /app
# "ruby-on-rail.rb" is the filename in the folder /app
ruby ruby-on-rail.rb

# after testing the ruby script inside the container, stop and delete the container
docker container stop myruby 
docker container rm myruby
```

NOTE: another possibile alternative to "sleep infinity" to keep the ruby container running:
```bash
# Keep container alive is through "tail" command
docker run -d --name myruby -v "$PWD":/app -w /app ruby:3.3 tail -f /dev/null
```


## Dockerfile
This Dockerfile is designed for a Ruby on Rails application with PostgreSQL.
This project needs these files:
```console
your-rails-app/
├── Dockerfile          # This file
├── Gemfile             # Rails dependencies
├── Gemfile.lock        # Locked gem versions
├── app/                # Rails app code
├── config/             # Rails configuration
└── db/                 # Database files
```


File: **Dockerfile**
```dockerfile
# Use Ruby 3.3 as base image
FROM ruby:3.3

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
# -qq: quiet mode for apt-get
# nodejs: JavaScript runtime needed by Rails
# postgresql-client: PostgreSQL client libraries
RUN apt-get update -qq && apt-get install -y \
    nodejs \
    postgresql-client

# Copy Gemfile and Gemfile.lock first for better layer caching
COPY Gemfile* ./

# Install Ruby gems defined in Gemfile
RUN bundle install

# Copy the rest of the application code
COPY . .

# Expose port 3000 for the Rails server
EXPOSE 3000

# Start Rails server bound to all network interfaces
# -b 0.0.0.0: makes the server accessible from outside the container
CMD ["rails", "server", "-b", "0.0.0.0"]
```

Run:
```bash
docker run -p 3000:3000 ruby-rails-app
```

## Project layout
layout:
```console
.
├── Dockerfile
├── Gemfile
├── Gemfile.lock        # optional on first run
└── main.rb
```

### Ruby script

File **main.rb**:

```Ruby
# A tiny Ruby program
def greet(name = "world")
  "Hello, #{name}!"
end

puts greet
```

Dependecies **Gemfile**
File: **Gemfile**
```Ruby
# Pin Ruby and gems for reproducibility
ruby "3.3.0"

source "https://rubygems.org"

# For a basic script you may not need any gems.
# Here's an example dependency you can try:
gem "colorize", "~> 1.1"
```

### Dockerfile
File: **Dockerfile**:
```dockerfile

# Use a small Ruby base image
FROM ruby:3.3-alpine

# Create non-root user for better security
RUN adduser -D appuser

# Install build tools only if you have native extensions
# (safe to keep; remove if not needed)
RUN apk add --no-cache build-base

# Set working directory
WORKDIR /app

# Copy dependency manifests first for cached bundle layer
COPY Gemfile Gemfile.lock ./
RUN bundle install --jobs=4 --retry=3

# Copy the rest of the app
COPY . .

# Drop privileges
USER appuser

# Default command: run the script; pass a name with `docker run ... Fabrizio`
CMD ["ruby", "main.rb"]
```

### Build & run
```Bash
# Build the image
docker build -t ruby-script .

# Run it (argument is optional)
docker run --rm ruby-script Fabrizio
# -> Hello, Fabrizio!
```

### One‑liner (no Dockerfile)
For quick tests, you can run a Ruby script directly using the official image:
```Bash
#  -v "$PWD":/app mounts your current directory
#  -w /app sets the working directory in the container
docker run --rm -v "$PWD":/app -w /app ruby:3.3 ruby main.rb John
```

### Nice‑to‑have files
File: **.dockerignore**
```dockerfile
.git
log/*
tmp/*
node_modules
vendor/bundle
```

### Optional: Compose for iterative dev
If you want to run and edit your script live: <br>

File: **docker-compose.yml**
```dockerfile
version: "3.9"
services:
  app:
    image: ruby:3.3-alpine
    working_dir: /app
    volumes:
      - .:/app
    command: ruby main.rb John
```
Run docker compose"
```bash
docker compose up --build
```


## Using Docker Compose (Rails + DB example)
File: **docker-compse.yml**
```dockerfile

version: "3.9"

services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: password

```

## .dockerignore
```console
.git
log/*
tmp/*
node_modules
```


## Best practices (worth following)

- Copy Gemfile separately for caching
- Use alpine for smaller images
- Pin Ruby version (ruby:3.3)
- Don’t run as root for production
- Use **.dockerignore**

