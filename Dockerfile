# Milestone 2: Dockerfile for Spark RAPIDS Development

# Base Image: Use a specific, versioned NVIDIA CUDA development image.
# Ubuntu 22.04 is a modern LTS, and CUDA 12.1.1 is a stable choice for recent RAPIDS versions.
FROM nvidia/cuda:12.8.0-devel-ubuntu22.04

# Set non-interactive mode for package installers
ENV DEBIAN_FRONTEND=noninteractive

# Install essential system dependencies and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    unzip \
    software-properties-common \
    # Clean up apt cache to keep image size down
    && rm -rf /var/lib/apt/lists/*

# Install Java (OpenJDK 11) and Maven for Spark/RAPIDS plugin builds
RUN apt-get update && apt-get install -y openjdk-11-jdk maven && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Install Miniconda for Python environment management
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh && \
    /opt/conda/bin/conda clean -tip

# Add conda to the PATH for all users
ENV PATH /opt/conda/bin:$PATH

# Create a non-root user for development to avoid permission issues with mounted volumes.
# Use ARG to allow build-time customization if needed.
ARG USER_ID=1000
ARG GROUP_ID=1000
ARG USER_NAME=dev
RUN groupadd -g $GROUP_ID $USER_NAME && \
    useradd -u $USER_ID -g $GROUP_ID -m -s /bin/bash $USER_NAME

# Switch to the new user
USER $USER_NAME
WORKDIR /home/$USER_NAME

# Set up conda for the new user
RUN conda init bash

# Set a default command to keep the container running if needed,
# but it will usually be overridden by `docker run -it ... /bin/bash`
CMD ["/bin/bash"]