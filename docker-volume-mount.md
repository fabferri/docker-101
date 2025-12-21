# Docker Volume mount

Docker has three types of volume mounts: **Named Volumes**, **Bind Mounts**, **Anonymous Volumes**.

## **Named Volumes** (created and managed by Docker)
Named volumes are managed by Docker and persist independently of containers. <br>
**Why use volumes:**
- **Persist data** beyond container lifecycle (databases, uploads, logs)
- **Share data** between containers
- **Avoid rebuilds** during development by mounting source code
- **Better performance** than bind mounts on Windows/Mac
```bash
#Stored in Docker's directory (/var/lib/docker/volumes/ on Linux)
#Persist independently of containers
docker run -v myvolume:/app nginx
```

## **Bind Mounts** (host directory)
Maps a specific host directory to container with direct access to host filesystem.

```bash
docker run -v /host/path:/container/path nginx

# Mount current directory to /app in container
# What each part does:
#   docker run - creates and runs a container
#   -v $(pwd):/app - mounts a volume:
#   $(pwd) - your current working directory on the host
#   :/app - mapped to /app inside the container
#   ubuntu - the image to use
#   ls /app - command executed inside the container
docker run -v $(pwd):/app ubuntu ls /app

# Mount with read-only access
docker run -v $(pwd):/app:ro ubuntu ls /app

# Named volume (persisted data)
docker run -d -v mydata:/var/lib/mysql mysql
```

## **Anonymous Volumes** (temporary)
- Created automatically without a name
- Docker generates a random ID
- **Removed when:**
  - Container is run with `--rm` flag (removed on container exit)
  - Container is removed with `-v` flag: `docker rm -v <container>`
  - Running `docker volume prune` (removes all unused volumes)
- **NOT removed** when using `docker rm <container>` alone (volume persists as orphaned)
- they persist as orphaned volumes if you just use `docker rm` without the `-v` flag.
- Best for temporary data

```bash
# Anonymous volume created automatically
docker run -v /app nginx

# Auto-remove container AND anonymous volume on exit
docker run --rm -v /app nginx

# Remove container and its anonymous volumes
docker rm -v <container_id>
```

## Volume management commands


Use these commands to create, inspect, and clean up volumes:

```bash
docker volume create myvolume       # create a named volume
docker volume ls                    # list all volumes
docker volume inspect myvolume      # inspect volume details (location, driver, mount point)
docker volume rm myvolume           # remove a volume (only works if not in use)
docker volume prune                 # remove all unused volumes (frees disk space)
```

Create a named volume for Nginx static pages
```bash
# Step 1: Create a named volume
docker volume create nginx-html

#Step 2: Create a temporary container to add HTML files to the volume
# Run a temporary nginx container with the volume mounted
docker run -d --name temp-nginx -v nginx-html:/usr/share/nginx/html nginx

# Step 3: Create your static HTML file
# Copy a custom HTML file into the container (which writes to the volume)
echo "<h1>Hello from my Nginx volume!</h1><p>This is stored in a named volume.</p>" > index.html
docker cp index.html temp-nginx:/usr/share/nginx/html/index.html

# Step 4: Stop and remove the temporary container
docker rm -f temp-nginx

# Step 5: Run a new Nginx container with the volume
docker run -d -p 8080:80 -v nginx-html:/usr/share/nginx/html --name my-nginx nginx

# Step 6: Test your static page
# Open in browser or use curl
curl http://localhost:8080

#Verify the volume persists:
# Remove the container
docker rm -f my-nginx

# Run a new container with the same volume
docker run -d -p 8080:80 -v nginx-html:/usr/share/nginx/html --name my-nginx-new nginx

# Your HTML file is still there!
curl http://localhost:8080

# Inspect the volume:
docker volume inspect nginx-html
```
The data in nginx-html volume persists independently of containers!

Example to recreate the container with different port mappings, keeping data by named volumes:
```bash
# Original container with volume
docker run -d -p 8080:80 -v mydata:/usr/share/nginx/html --name web1 nginx

# Stop and remove
docker rm -f web1

# Recreate with different port, same volume
docker run -d -p 9090:80 -v mydata:/usr/share/nginx/html --name web2 nginx
```


**Note** <br>
Volumes can only be removed when no containers (running or stopped) are using them:<br>

```bash
# step1: Find which containers are using the volume
docker ps -a --filter volume=myvolume

# step2: Stop the container(s)
docker stop <container_id>

# step3: Remove the container(s)
docker rm <container_id>

# step4: Now remove the volume
docker volume rm myvolume
```

Another alternative way to do it:
```bash
# See which containers use the volume
docker volume inspect myvolume

# Force remove running container
docker rm -f <container_id>

# Then remove volume
docker volume rm myvolume
```

---

## Next step

[Docker networking](docker-networking.md)

Coming back to the table of contents: [Docker 101: first hands-on](README.md)
