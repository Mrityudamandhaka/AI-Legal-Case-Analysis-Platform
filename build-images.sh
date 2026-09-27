#!/bin/bash

# LawMind Docker Build Script

echo "Building LawMind Docker Images"

# Build backend
echo "Building backend..."
docker build -t lawmind-backend -f docker/Dockerfile.backend . --load

# Check if backend build was successful
if [ $? -eq 0 ]; then
    echo "Backend build successful"
else
    echo "Backend build failed"
    exit 1
fi

# Build frontend
echo "Building frontend..."
docker build -t lawmind-frontend -f docker/Dockerfile.frontend . --load

# Check if frontend build was successful
if [ $? -eq 0 ]; then
    echo "Frontend build successful"
else
    echo "Frontend build failed"
    exit 1
fi

echo "All images built successfully!"