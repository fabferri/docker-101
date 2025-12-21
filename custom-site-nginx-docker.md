#  Docker container running NGINX that serves a custom static website

## Prerequisites
Make sure you have Docker installed: `docker --version`

## Step 1: Create the project folder

```bash
mkdir nginx-static-site
cd nginx-static-site
```

## Step 2: Create the static website

Create a folder for your site files:
```bash
mkdir html
```
Create a sample page:
```bash
vim html/index.html
```
Example content:
```html
<!DOCTYPE html>
<html>
<head>
  <title>My Static Site</title>
  <style>
    body { font-family: Arial; text-align: center; margin-top: 50px; }
  </style>
</head>
<body>
  <h1>Hello from NGINX + Docker </h1>
  <p>This is a custom static website.</p>
</body>
</html>
```

## Step 3: Create the NGINX config

Create the file: `vim default.conf` and paste this static-only NGINX configuration:
```
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location = /healthz {
        return 200 'ok';
        add_header Content-Type text/plain;
    }
}
```

## Step 4: Create the Dockerfile
Create the file: `vim Dockerfile` and paste the following content:
```
FROM nginx:alpine

# Remove default NGINX config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom config
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy static site
COPY html/ /usr/share/nginx/html/

# Expose HTTP
EXPOSE 80

# Run NGINX
CMD ["nginx", "-g", "daemon off;"]

```

## Step 5: Build the Docker image
From inside nginx-static-site:

```bash
docker build -t my-static-site .
```

Verify: `docker images | grep my-static-site`

## Step 6: Run the container
- Container name: nginx-static
- Website exposed on port 8080

```bash
docker run -d \
  --name nginx-static \
  -p 8080:80 \
  my-static-site

```

## Step 7: Test the site
Open in browser: `http://localhost:8080`
Health check: `curl http://localhost:8080/healthz`
the output should be `ok`

### Step 8: Update the site (two options)

Option A — Rebuild image (recommended for prod)
```bash
docker stop nginx-static
docker rm nginx-static
docker build -t my-static-site .
docker run -d -p 8080:80 my-static-site
```

### Option B — Live edit files (dev only)
```bash

docker run -d \
  -p 8080:80 \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  nginx:alpine
```

## Step 9: Stop and clean up

```bash
docker stop nginx-static
docker rm nginx-static
```

## Final folder structure
```
nginx-static-site/
├── Dockerfile
├── default.conf
└── html/
    └── index.html
```
