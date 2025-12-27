# Working with registries

## Table of Contents

- [Working with Docker Hub](#working-with-docker-hub)
- [Create private Azure Container Registry](#create-private-azure-container-registry)
- [Access the ACR through Admin User](#access-the-acr-through-admin-user)
- [Push a local image to the registry](#push-a-local-image-to-the-registry)
- [View images in ACR](#view-images-in-acr)
- [Remove tags from local Docker images](#remove-tags-from-local-docker-images)
- [Access ACR using User-Assigned Managed Identity (MSI) via Azure CLI](#access-acr-using-user-assigned-managed-identity-msi-via-azure-cli)

---
**NOTE** <br>
in this article replace: <br>
**yourusername** -> your username to access to of the Docker Hub <br>
**yourpassword** -> your password to access to of the Docker Hub <br>

**yourcontainerregistryname** -> the name of your ACR container name <br>
**yourResourceGroup** -> the name of your Aziure Resource Group
---

## Working with Docker Hub

Docker Hub is the default public registry for Docker images.

```bash
# Pull/download an image from Docker Hub
docker pull <image-name>:<tag>

# Examples to pull images from docker hub to local host:
docker pull nginx:latest         # Pull latest nginx image
docker pull mysql:8.0            # Pull MySQL version 8.0
docker pull ubuntu:22.04         # Pull Ubuntu 22.04
docker pull redis:alpine         # Pull Redis with Alpine Linux

# If no tag is specified, 'latest' is assumed
docker pull nginx                # Same as nginx:latest

# View downloaded images in local host
docker images

# Login to Docker Hub (required for private repos or to avoid rate limits)
docker login
# Enter your Docker Hub username and password
# a shorter way to login: docker login -u <username>

# Pull a private image (after login)
docker pull yourusername/private-repo:tag

# Push an image to Docker Hub
# Step 1: Tag your local image with your Docker Hub username
docker tag myapp:latest yourusername/myapp:latest
docker tag nginx:latest yourusername/nginx:v1

# Step 2: Push the tagged image to Docker Hub
docker push yourusername/myapp:latest
docker push yourusername/nginx:v1

# View images in Docker Hub repositories

# For local images (already pulled):
docker images                     # Show all local images
docker images yourusername/myapp  # Show specific repository images locally
docker images yourusername/nginx  # Show specific repository images locally

# -------------------------------------------------
# VIEW images in your PRIVATE Docker Hub repository:
# IMPORTANT: Docker CLI has NO native command to list remote repository images
# You must use one of these methods:

# Method 1: Docker Hub Website (easiest)
# - Visit https://hub.docker.com
# - Login with your credentials
# - Navigate to your repositories
# - View: https://hub.docker.com/u/yourusername/

# Method 2: Docker Hub API (programmatic)
# Get authentication token
TOKEN=$(curl -s -H "Content-Type: application/json" \
  -X POST -d '{"username":"yourusername","password":"yourpassword"}' \
  https://hub.docker.com/v2/users/login/ | jq -r .token)

# List all repositories in your account
curl -s -H "Authorization: JWT ${TOKEN}" \
  https://hub.docker.com/v2/repositories/yourusername/ | jq

# Example with real username:
curl -s -H "Authorization: JWT ${TOKEN}" \
  https://hub.docker.com/v2/repositories/yourusername/ | jq

# Get just the repository names
curl -s -H "Authorization: JWT ${TOKEN}" \
  https://hub.docker.com/v2/repositories/yourusername/ | jq -r '.results[].name'

# List tags for a specific repository (once you know the repository name)
curl -s -H "Authorization: JWT ${TOKEN}" \
  https://hub.docker.com/v2/repositories/yourusername/myapp/tags/ | jq

# Example:
curl -s -H "Authorization: JWT ${TOKEN}" \
  https://hub.docker.com/v2/repositories/yourusername/nginx/tags/ | jq

# Get just the tag names for a repository
curl -s -H "Authorization: JWT ${TOKEN}" \
  https://hub.docker.com/v2/repositories/yourusername/nginx/tags/ | jq -r '.results[].name'

# Method 3: Pull the image to view locally
docker login
docker pull yourusername/private-repo:tag
docker pull yourusername/nginx:v1   # pull image from private docker hub to local image

# View images in repositories
# Show all local images
docker images

# Show images for a specific repository (local)
docker images nginx
docker images yourusername/nginx


# Note: Docker CLI has no native command to list all images in a remote repository
# To view your images on Docker Hub:
# - Visit https://hub.docker.com and login to see your repositories
# - Use Docker Hub API for programmatic access
# - Use web browser to view: https://hub.docker.com/r/yourusername/repository-name/tags

# Delete images from Docker Hub

# IMPORTANT: Docker CLI has NO command to delete images from Docker Hub
# You can only delete LOCAL images with 'docker rmi'
# To delete from Docker Hub, use one of these methods:

# Method 1: Docker Hub Website (easiest)
# 1. Visit https://hub.docker.com
# 2. Login with your credentials
# 3. Navigate to Repositories
# 4. Click on the repository name
# 5. Go to "Tags" tab
# 6. Click the trash icon next to the tag to delete
# 7. To delete entire repository: Settings -> Delete repository

# Method 2: Docker Hub API (programmatic)
# Get authentication token first
TOKEN=$(curl -s -H "Content-Type: application/json" \
  -X POST -d '{"username":"yourusername","password":"yourpassword"}' \
  https://hub.docker.com/v2/users/login/ | jq -r .token)

# Delete a specific tag from a repository
curl -X DELETE \
  -H "Authorization: JWT ${TOKEN}" \
  https://hub.docker.com/v2/repositories/yourusername/myapp/tags/v1.0/

# Example: Delete nginx:v1 tag
curl -X DELETE \
  -H "Authorization: JWT ${TOKEN}" \
  https://hub.docker.com/v2/repositories/yourusername/nginx/tags/v1/

# Delete entire repository (use with caution!)
curl -X DELETE \
  -H "Authorization: JWT ${TOKEN}" \
  https://hub.docker.com/v2/repositories/yourusername/nginx/

# Note: Deleting a tag does NOT delete it from Docker Hub immediately
# Docker Hub may take some time to clean up the underlying layers

# To delete LOCAL images (not from Docker Hub):
docker rmi yourusername/myapp:latest       # Remove local image
docker rmi yourusername/nginx:latest           # Remove local image

# Logout from Docker Hub
docker logout
```

---

# Create private Azure Container Registry

Azure Container Registry (ACR) is a private registry service for building, storing, and managing container images. An ACR can be created by Azure CLI:

```bash
# Create a resource group
az group create --name yourResourceGroup --location uksouth

# Create an ACR with internet access (private but publicly accessible)
# --public-network-enabled true, which:
#     Allows access from the internet
#     Still requires authentication (private registry)
#     Can be accessed via public IP without requiring DNS resolution
# NOTE: ACR names must be globally unique across Azure (3-50 lowercase alphanumeric characters)
az acr create --resource-group yourResourceGroup \
  --name yourcontainerregistryname --sku Basic \
  --public-network-enabled true

# Get the ACR login server endpoint
az acr show --name yourcontainerregistryname \
  --resource-group yourResourceGroup \
  --query loginServer --output table
```

## Access the ACR through Admin User

There are multiple ways to authenticate to Azure Container Registry. <br>
Access through ACR Admin User is simple but less secure.

```bash
# Enable admin user on the ACR
az acr update --name yourcontainerregistryname \
  --resource-group yourResourceGroup \
  --admin-enabled true

# Get admin credentials
az acr credential show --name yourcontainerregistryname \
  --resource-group yourResourceGroup 

# The command show Username and Password to access to the ACR.

# Login with Docker using username and password
docker login yourcontainerregistryname.azurecr.io

# digit Username and Password as shown from the command "az acr credential show"
# Username: yourcontainerregistryname
# Password: <from credential show command>
```

## Push a local image to the registry
Steps for pushing local images to ACR:

- List local images to see what's available
- Tag the image with the ACR login server name (the tagging step is crucial!)
- Push the image to the registry
- Verify the push using az acr repository commands

```bash
# List local images to find your image
docker images

# Tag your local image with the ACR login server name
# Format: docker tag <local-image>:<tag> <acr-login-server>/<image-name>:<tag>
docker tag myapp:latest yourcontainerregistryname.azurecr.io/myapp:v1

# Push the tagged image to ACR
docker push yourcontainerregistryname.azurecr.io/myapp:v1

# Another example, if your local image "nginx:latest" and you tag with "nginx:v1"
docker tag nginx:latest yourcontainerregistryname.azurecr.io/nginx:v1

# Push the tagged image to ACR
docker push yourcontainerregistryname.azurecr.io/nginx:v1

# let assume that you have the docker image stored in the volume called "mysql:latest"
docker tag mysql:latest yourcontainerregistryname.azurecr.io/mysql

# Push the tagged image to ACR
docker push yourcontainerregistryname.azurecr.io/mysql

# Verify the image was pushed to ACR
az acr repository list --name yourcontainerregistryname --output table

# Show tags for a specific image
az acr repository show-tags --name yourcontainerregistryname \
  --repository myapp --output table

# Show detailed information about a specific image/tag
az acr repository show --name yourcontainerregistryname \
  --repository myapp --output table

# List all manifests for an image
az acr manifest list-metadata --name yourcontainerregistryname \
  --repository myapp --output table


```

## View images in ACR

Note: Docker doesn't have a native command to list remote registry images. Use Azure CLI instead:

```bash
# List all repositories (images) in ACR
az acr repository list --name yourcontainerregistryname --output table

# Show all tags for a specific repository
az acr repository show-tags --name yourcontainerregistryname \
  --repository mysql --output table

# Show detailed metadata for a repository
az acr repository show --name yourcontainerregistryname \
  --repository mysql
```

## Remove tags from local Docker images

**Note:** Removing image tags is a Docker operation, not an Azure CLI command.

```bash
# Remove a specific tag from a local image
# This only removes the tag, not the actual image (unless it's the last tag)
docker rmi yourcontainerregistryname.azurecr.io/mysql:latest

# Alternative syntax
docker image rm yourcontainerregistryname.azurecr.io/mysql:latest

# List images to see remaining tags
docker images

# Remove multiple tags at once
docker rmi yourcontainerregistryname.azurecr.io/mysql:latest \
  yourcontainerregistryname.azurecr.io/nginx:v1

# Force remove (if image is being used by a stopped container)
docker rmi -f yourcontainerregistryname.azurecr.io/mysql:latest

# Remove untagged images (images with <none> tag)
docker image prune

# Example workflow: After pushing to ACR, remove the local ACR tag
docker tag mysql:8.0 yourcontainerregistryname.azurecr.io/mysql:latest  # Creates tag
docker push yourcontainerregistryname.azurecr.io/mysql:latest           # Push to ACR
docker rmi yourcontainerregistryname.azurecr.io/mysql:latest            # Remove local ACR tag
# The original mysql:8.0 tag remains on your local machine
```

**Important notes:**
- `docker rmi` only removes the **tag/reference**, not necessarily the image data
- If an image has multiple tags, removing one tag won't delete the image
- The actual image is only deleted when **all tags** pointing to it are removed
- Use `docker images` to see which tags remain after removal



## Access ACR using User-Assigned Managed Identity (MSI) via Azure CLI

Managed identities provide Azure services with an automatically managed identity for authentication without credentials.

```bash
# Step 1: Create a user-assigned managed identity
az identity create --name myACRIdentity \
  --resource-group yourResourceGroup

# Step 2: Get the identity details
IDENTITY_ID=$(az identity show \
  --resource-group yourResourceGroup \
  --name myACRIdentity \
  --query id --output tsv)

IDENTITY_CLIENT_ID=$(az identity show \
  --resource-group yourResourceGroup \
  --name myACRIdentity \
  --query clientId --output tsv)


# Step 3: Assign AcrPull role to the managed identity for pulling images
az role assignment create \
  --assignee $IDENTITY_PRINCIPAL_ID \
  --role AcrPull \
  --scope $(az acr show --name yourcontainerregistryname \
    --resource-group yourResourceGroup --query id --output tsv)

# Step 4: For pushing images, assign AcrPush role
az role assignment create \
  --assignee $IDENTITY_PRINCIPAL_ID \
  --role AcrPush \
  --scope $(az acr show --name yourcontainerregistryname \
    --resource-group yourResourceGroup --query id --output tsv)

# Step 5: For Pull, push, and delete images, assign AcrDelete role
az role assignment create \
  --assignee $IDENTITY_PRINCIPAL_ID \
  --role AcrDelete \
  --scope $(az acr show --name yourcontainerregistryname \
    --resource-group yourResourceGroup --query id --output tsv)

# Step 6: Login to ACR using the managed identity
# IMPORTANT: This ONLY works when executed from Azure resources with managed identity
# Where can you use `--identity` flag
# - Works from: 
#      - Azure VM with assigned managed identity
#      - Azure Cloud Shell with managed identity
#      - AKS nodes or pods with managed identity
#      - Azure Container Instances with managed identity
#      - Other Azure services configured with managed identity
# - Does NOT work from: Local machine, on-premises servers, non-Azure environments

# Get resource ID and use the identity
IDENTITY_CLIENT_ID=$(az identity show \
  --resource-group yourResourceGroup \
  --name myACRIdentity \
  --query clientId --output tsv)

# Using user-assigned managed identity (requires client ID)
# Only works on Azure VM/service with this user-assigned identity attached
az acr login --name yourcontainerregistryname --identity $IDENTITY_CLIENT_ID

# Step 7: Verify access (only after successful login from Azure resource)
az acr repository list --name yourcontainerregistryname --output table
```

---

## Next step

[Docker compose](08-compose.md)

## Coming back

[Docker 101: first trek](README.md)