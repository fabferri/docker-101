# Node.js Web Application Example

A simple Node.js web server demonstrating Docker containerization for web applications.

## What's Inside

- `server.js` - A basic HTTP server built with Node.js
- `package.json` - Node.js project configuration
- `Dockerfile` - Multi-layer Docker image configuration

## How to Use

### Build the Docker image

```bash
cd webapp
docker build -t my-webapp .
```

### Run the container

```bash
docker run -d -p 3000:3000 --name webapp my-webapp
```

### Access the application

Open your browser and visit: http://localhost:3000

### View logs

```bash
docker logs webapp
```

### Stop the container

```bash
docker stop webapp
docker rm webapp
```

## Development with Volume Mounts

For live development without rebuilding:

```bash
docker run -d -p 3000:3000 -v $(pwd):/app --name webapp-dev my-webapp
```

Now you can edit `server.js` on your host machine, and the changes will be reflected in the container!

## Learning Points

1. **Base Image** - Uses `node:18-alpine` (lightweight Node.js image)
2. **Working Directory** - All commands execute in `/app`
3. **Dependency Installation** - Copies package.json first (better layer caching)
4. **Port Exposure** - Exposes port 3000 for the web server
5. **Port Mapping** - Maps host port 3000 to container port 3000

## Health Check

The app includes a health check endpoint: http://localhost:3000/health
