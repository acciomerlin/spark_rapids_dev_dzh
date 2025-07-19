#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Define image name and tag
IMAGE_NAME="spark-rapids-dev"
IMAGE_TAG="latest"

# Get the directory of the script to robustly find the Dockerfile
SCRIPT_DIR=$(dirname "$(realpath "$0")")
CONTEXT_DIR=$(dirname "$SCRIPT_DIR")

echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "Dockerfile location: ${CONTEXT_DIR}/Dockerfile"

# Build the Docker image, passing current user's UID/GID to the build process
# so the user inside the container has the same permissions.
docker build \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP_ID=$(id -g) \
    --build-arg USER_NAME=$(whoami) \
    -t "${IMAGE_NAME}:${IMAGE_TAG}" \
    "${CONTEXT_DIR}"

echo "Build complete."
echo "Image available as: ${IMAGE_NAME}:${IMAGE_TAG}"