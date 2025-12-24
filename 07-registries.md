# Working with registries

```bash
# Login to Docker Hub
docker login

# Login to Azure Container Registry
docker login myregistry.azurecr.io

# Tag image for registry
docker tag myapp:latest myregistry.azurecr.io/myapp:v1

# Push to registry
docker push myregistry.azurecr.io/myapp:v1

# Pull from private registry
docker pull myregistry.azurecr.io/myapp:v1

# Logout
docker logout
```

---

## Next step

[Docker compose](08-compose.md)

## Coming back

[Docker 101: first trek](README.md)