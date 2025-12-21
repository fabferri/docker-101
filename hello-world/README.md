# Hello World Docker Example

A simple Python application demonstrating basic Docker concepts.

## What's Inside

- `app.py` - A simple Python script that prints a hello message
- `Dockerfile` - Instructions to build a Docker image

## How to Use

### Build the Docker image

```bash
cd hello-world
docker build -t hello-world-app .
```

### Run the container

```bash
docker run hello-world-app
```

You should see a hello message with the current timestamp!

## Learning Points

1. **FROM** - We use `python:3.11-slim` as the base image (smaller than full Python image)
2. **WORKDIR** - Sets `/app` as the working directory
3. **COPY** - Copies `app.py` from your host to the container
4. **CMD** - Defines the command to run when the container starts

## Next Steps

Try modifying `app.py` to print your own message, then rebuild and run the container!
