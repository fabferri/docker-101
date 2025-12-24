# Docker networking (basics)

Custom networks allow:

- Container isolation, containers on different networks can't communicate
- Name-based discovery, containers can reach each other using container names instead of IP addresses
- Better control, manage which containers can talk to each other
Custom networks are essential for multi-container applications where containers need to communicate using predictable names.

Network types:

- **bridge** (default) - created automatically, used by `docker network create`
- **host** - container shares host's network stack
- **none** - no networking

```bash
# List networks
docker network ls

# Create a custom network
# Creates a user-defined bridge network
# Allows containers on this network to communicate with each other
# Provides automatic DNS resolution between containers (containers can reach each other by name)
docker network create mynetwork

# Run containers on the same network
docker run -d --name web --network mynetwork nginx
docker run -d --name api --network mynetwork node
# Now 'web' container can reach 'api' container by name:
docker exec web ping api

# List all networks
docker network ls

# Inspect network
docker network inspect mynetwork

# Connect an existing running (or stopped) container to a network
docker network connect mynetwork container_name

# Disconnect from network
docker network disconnect mynetwork container_name

# Remove network
docker network rm mynetwork
```

Connect a container that was started without a network:
```bash
# Container started on default bridge network
docker run -d --name web nginx

# Later, connect it to custom network
docker network connect mynetwork web
```

Connect a container to multiple networks:
```bash
# Start on one network
docker run -d --name app --network frontend-net nginx

# Add to another network
docker network connect backend-net app

# Now 'app' is on both frontend-net AND backend-net
```

Enable communication between containers:
```bash
# Database on custom network
docker run -d --name db --network mynetwork postgres

# Web app on default network
docker run -d --name webapp nginx

# Connect webapp to mynetwork so it can reach db
docker network connect mynetwork webapp

# Now webapp can connect to db using: postgresql://db:5432

# Verify connection:
docker network inspect mynetwork    # See all connected containers
docker inspect webapp               # See all networks webapp is on

# Disconnect:
docker network disconnect mynetwork webapp
```
This is useful for adding containers to networks after they've been created, without restarting them.

---

## Next step

[Deploy a Custom Static Website with Docker and Nginx](05-custom-site-nginx-docker.md)

## Coming back

[Docker 101: first trek](README.md)