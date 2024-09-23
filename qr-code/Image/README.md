# Multi-platform QR Code Generator Docker Image Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Functionality](#functionality)
4. [Building Multi-platform Images](#building-multi-platform-images)
5. [Pushing to Docker Hub](#pushing-to-docker-hub)
6. [Using the Image](#using-the-image)
7. [Troubleshooting](#troubleshooting)

## Introduction

This guide walks you through the process of building a multi-platform Docker image for a QR code generator application, pushing it to Docker Hub, and explains the functionality of the image.

## Prerequisites

- Docker installed on your machine
- Docker Hub account
- Docker Buildx (included with Docker Desktop and recent versions of Docker)
- Git (optional, for version control)

## Functionality

The QR code generator Docker image contains a FastAPI application that:

1. Provides a simple web interface for users to input text or URLs.
2. Generates QR codes based on the input.
3. Displays the generated QR code in the browser.
4. Offers an API endpoint for programmatic QR code generation.

The application is designed to handle high loads and uses caching to improve performance.

## Building Multi-platform Images

1. Create a new `Dockerfile` in your project root:

```dockerfile
FROM --platform=$BUILDPLATFORM python:3.9-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "8", "--loop", "uvloop", "--http", "httptools"]
```

This Dockerfile uses a multi-stage build to reduce the final image size and avoid architecture-specific build issues.

2. Set up Docker Buildx:

```bash
docker buildx create --name mybuilder --use
```

3. Build and push the multi-platform image:

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
  -t yourusername/qr-code-generator:latest \
  --push .
```

Replace `yourusername` with your Docker Hub username. Note that we've removed `linux/arm/v7` from the platforms list to avoid the error you encountered.

## Pushing to Docker Hub

The previous command already pushes the image to Docker Hub. If you want to push a new tag:

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
  -t yourusername/qr-code-generator:v1.0 \
  --push .
```

## Using the Image

To use the image:

```bash
docker run -p 8080:8080 yourusername/qr-code-generator:latest
```

Access the application at `http://localhost:8080`.

## Troubleshooting

If you encounter issues:

1. Check Docker logs:
   ```bash
   docker logs <container-id>
   ```

2. Ensure all files are correctly placed in the Docker context.

3. Verify that the `templates` directory and `index.html` file are present in the image:
   ```bash
   docker run -it --rm yourusername/qr-code-generator:latest /bin/bash
   ls -R /app
   ```

4. If you encounter platform-specific issues, try building for a single platform first:
   ```bash
   docker buildx build --platform linux/amd64 \
     -t yourusername/qr-code-generator:latest-amd64 \
     --push .
   ```

5. If you need to support `linux/arm/v7`, you may need to use a different base image or create a separate Dockerfile for that architecture.

6. Make sure your `requirements.txt` file doesn't include any architecture-specific packages.

7. If changes are needed, rebuild and push the image with a new tag.

For more detailed troubleshooting, refer to the Docker and FastAPI documentation.