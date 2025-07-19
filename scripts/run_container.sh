#!/bin/bash
set -e

IMAGE_NAME="spark-rapids-dev:latest"
CONTAINER_NAME="rapids_dev_env"
PROJECT_DIR=~/spark_rapids_dev

# Check if a container with the same name is already running
if [ "$(docker ps -q -f name=^/${CONTAINER_NAME}$)" ]; then
    echo "Attaching to running container: ${CONTAINER_NAME}"
    docker exec -it "${CONTAINER_NAME}" /bin/bash
    exit 0
fi

echo "Starting new container: ${CONTAINER_NAME}"

docker run -it --rm \
    --name "${CONTAINER_NAME}" \
    --gpus all \
    --shm-size=4g \
    -v "${PROJECT_DIR}/source:/home/$(whoami)/source" \
    -v "${PROJECT_DIR}/cache/m2_cache:/home/$(whoami)/.m2" \
    -v "${PROJECT_DIR}/cache/ccache:/home/$(whoami)/.ccache" \
    -v "${PROJECT_DIR}/cache/conda_cache:/home/$(whoami)/.conda/pkgs" \
    -v "${PROJECT_DIR}/data:/home/$(whoami)/data" \
    "${IMAGE_NAME}" \
    /bin/bash