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
# Run a basic nginx container in the foreground with a custom name
#   docker run - creates and starts a new container
#   --name my-nginx - assigns the name "my-nginx" to the container
#   nginx - the image to use
# Container is terminated on CRL-C or exit
docker run --name my-nginx nginx

# In another terminal, connect to the running container interactively
#   docker exec - executes a command in a running container
#   -it - interactive mode with pseudo-TTY (terminal)
#   my-nginx - the name of the container to connect to
#   bash - the command to run (opens a bash shell)
docker exec -it my-nginx  bash
```

Let's run a basic example of volume mount:

```bash
# Stored in Docker's directory (/var/lib/docker/volumes/ on Linux)
# Persist independently of containers
#   docker run - creates and starts a new container. 
#                "docker run" does not create a persistent/running container. It runs in the foreground.
#                he container stops when the nginx process exits or you press Ctrl+C
#   -v myvolume:/app - mounts a named volume:
#      myvolume - the named volume (created automatically if it doesn't exist)
#      :/app - mounted to /app directory inside the container
#   nginx - the image to use
docker run -v myvolume:/app nginx

# in another terminal connect to the container
docker exec -it <container_id>  bash

# inside the nginx container copy the nginx homepage to the /app
cp /usr/share/nginx/html/index.html /app

# stop the nginx container, exiting from the first terminal

# Start again a new  container (if not already running)
docker run -d --name my-nginx -v myvolume:/app nginx

# Connect to the container
docker exec -it my-nginx bash

# Inside the container, browse the /app directory to see 
# Check the presence of the file index.html - the file copied in the volume with first container
ls -la /app

# remove the container
docker rm -f my-nginx
```

## **Bind Mounts** (host directory)
Maps a specific host directory to container with direct access to host filesystem.

```bash

# Basic bind mount syntax
#   docker run - creates and starts a new container
#   -v /host/path:/container/path - creates a bind mount:
#      /host/path - absolute path to directory on your host machine (must exist)
#      :/container/path - path inside the container where host directory is mounted
#   nginx - the image to use
# Note: Changes made in either location (host or container) are immediately reflected in both
# docker run -v /host/path:/container/path nginx
docker run --name my-nginx -v /tmp:/tmp nginx

# in another terminal connect to the container and check the content in the folder /tmp by ls /tmp
docker exec -it my-nginx bash


# Mount current directory to /app in container
# What each part does:
#   docker run - creates and runs a container
#   -v $(pwd):/app - mounts a volume:
#      $(pwd) - your current working directory on the host (must exist)
#      :/app - mounted to /app inside the container (created automatically by Docker if it doesn't exist)
#   ubuntu - the image to use
#   ls /app - command executed inside the container
# Note: You don't need to create /app on the host - it's the container path where your host directory is mounted
docker run -v $(pwd):/app ubuntu ls /app


# Verify persistence of bind mount:
# Step 1: Create a file from inside a container
docker run --rm -v $(pwd):/app ubuntu sh -c "echo 'Hello from container' > /app/test.txt"

# Step 2: Container is automatically removed (--rm flag), but check the file persists on host
ls $(pwd)/test.txt        # File still exists on host
cat $(pwd)/test.txt       # Shows: Hello from container

# Step 3: Clean up
rm test.txt
```

Few options:
```bash
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

## Example: Named volume for Nginx static pages

Create a named volume for Nginx static pages:
```bash
# Step 1: Create a named volume
docker volume create nginx-html

#Step 2: Create a temporary container to add HTML files to the volume
# Run a temporary nginx container with the volume mounted
#   docker run - creates and starts a new container
#   -d - detached mode (runs in background)
#   --name temp-nginx - assigns name "temp-nginx" to the container
#   -v nginx-html:/usr/share/nginx/html - mounts the named volume:
#      nginx-html - the named volume created in Step 1
#      :/usr/share/nginx/html - mounted to Nginx's default HTML directory in the container
#   nginx - the image to use
docker run -d --name temp-nginx -v nginx-html:/usr/share/nginx/html nginx

# Step 3: Create your static HTML file
# Copy a custom HTML file "index.html" from local directory into the container (which writes to the volume)
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

## Removing volumes

Volumes can only be removed when no containers (running or stopped) are using them.

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

## Multiple containers sharing the same volume

Yes, multiple containers can mount and share the same volume simultaneously. This is useful for:

- Sharing configuration files across containers
- Log aggregation from multiple services
- Shared storage for microservices
- Data synchronization between containers

**Example: Multiple containers sharing the same volume**

```bash
# Create a shared volume
docker volume create shared-data

# Container 1: Writes data to the volume (includes hostname to identify the writer)
docker run -d --name writer1 -v shared-data:/data alpine sh -c "while true; do echo \"\$(hostname) - \$(date)\" >> /data/log.txt; sleep 5; done"

# Container 2: Writes data to the volume (includes hostname to identify the writer)
docker run -d --name writer2 -v shared-data:/data alpine sh -c "while true; do echo \"\$(hostname) - \$(date)\" >> /data/log.txt; sleep 5; done"

# Container 3: Reads from the same volume
docker run -d --name reader1 -v shared-data:/data alpine sh -c "while true; do tail -f /data/log.txt; sleep 5; done"

# Container 4: Also reads from the same volume
docker run -d --name reader2 -v shared-data:/data alpine sh -c "while true; do cat /data/log.txt; sleep 5; done"

# View logs from the reader containers
docker logs -f reader1
docker logs reader2

# Cleanup
docker rm -f writer reader1 reader2
docker volume rm shared-data
```

> [!NOTE]
> When multiple containers write to the same volume simultaneously, ensure your application handles file locking and concurrent access properly to avoid data corruption.

---

## Next step

[Build Dockerfile](03-dockerfile.md)

## Coming back

[Docker 101: first trek](README.md)
