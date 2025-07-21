#!/bin/bash
set -e

IMAGE_NAME="spark-rapids-dev:1.0.0"
CONTAINER_NAME="rapids_dev_env"
# Define the project directory on the host. This will be mounted to the same path inside the container.
PROJECT_DIR=$(realpath ~/spark_rapids_dev)
CONTAINER_PROJECT_DIR="/root/spark_rapids_dev"

# Ensure project directory and subdirectories exist
mkdir -p "${PROJECT_DIR}/source"
mkdir -p "${PROJECT_DIR}/data"
mkdir -p "${PROJECT_DIR}/cache/m2_cache"
mkdir -p "${PROJECT_DIR}/cache/ccache"
mkdir -p "${PROJECT_DIR}/cache/conda_cache"

# Check if a container with the same name is already running
if [ "$(docker ps -q -f name=^/${CONTAINER_NAME}$)" ]; then
    echo "Attaching to running container: ${CONTAINER_NAME}"
    docker exec -it "${CONTAINER_NAME}" /bin/bash
    exit 0
fi

echo "Starting new container: ${CONTAINER_NAME}"

docker run -it  \
    --name "${CONTAINER_NAME}" \
    --gpus all \
    -p 8080:8080 \
    -p 4040:4040 \
    --shm-size=4g \
    -v "${PROJECT_DIR}:${CONTAINER_PROJECT_DIR}" \
    -v "${PROJECT_DIR}/cache/m2_cache:/root/.m2" \
    -v "${PROJECT_DIR}/cache/ccache:/root/.ccache" \
    -v "${PROJECT_DIR}/cache/conda_cache:/root/.conda/pkgs" \
    -w "${CONTAINER_PROJECT_DIR}" \
    "${IMAGE_NAME}" \
    /bin/bash -c "echo 'export SPARK_HOME=${CONTAINER_PROJECT_DIR}/source/spark-3.5.6-bin-hadoop3' >> /root/.bashrc && echo 'export PATH=\$PATH:\$SPARK_HOME/bin:\$SPARK_HOME/sbin' >> /root/.bashrc && exec /bin/bash"