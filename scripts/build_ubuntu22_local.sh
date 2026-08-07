#!/usr/bin/env bash
# Builds a Linux executable inside an Ubuntu 22.04 container (glibc 2.35), so the
# resulting binary can run on Ubuntu 22.04 and newer.
#
# Usage: ./scripts/build_ubuntu22_local.sh
set -euo pipefail

APP_NAME="password-generator-ubuntu22"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE_TAG="password-generator-linux-builder"

echo "==> Checking for Docker..."
if ! command -v docker >/dev/null 2>&1; then
    echo "Docker is not installed. Install it first, then run this script again:"
    echo "  Debian/Ubuntu: sudo apt install docker.io"
    echo "  Fedora:        sudo dnf install docker"
    echo "  Arch:          sudo pacman -S docker"
    exit 1
fi
echo "    Found: $(docker --version)"

echo "==> Building (or reusing cached) builder image [$IMAGE_TAG] ..."
docker build -t "$IMAGE_TAG" -f - "$PROJECT_DIR" <<'EOF'
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
            python3.10 \
            python3.10-venv \
            python3.10-tk \
      python3-pip \
            libpython3.10 \
      binutils \
      ca-certificates && \
    rm -rf /var/lib/apt/lists/*
EOF

echo "==> Building executable inside the container ..."
docker run --rm \
    -v "$PROJECT_DIR":/work \
    -w /work \
    "$IMAGE_TAG" \
    bash -lc '
        set -euo pipefail
        python3.10 -m venv /tmp/buildvenv
        /tmp/buildvenv/bin/pip install --quiet --upgrade pip
        /tmp/buildvenv/bin/pip install --quiet uv

        rm -rf build dist
        /tmp/buildvenv/bin/uv pip install --python /tmp/buildvenv/bin/python customtkinter pyinstaller
        mkdir -p dist/ubuntu22
        /tmp/buildvenv/bin/pyinstaller \
            --noconfirm \
            --onefile \
            --windowed \
            --name "password-generator-ubuntu22" \
            --distpath dist/ubuntu22 \
            --workpath build/ubuntu22 \
            --specpath build/ubuntu22 \
            main.py

        echo "Build finished. Artifact: dist/ubuntu22/password-generator-ubuntu22"
    '

BINARY="$PROJECT_DIR/dist/ubuntu22/$APP_NAME"
if [[ ! -f "$BINARY" ]]; then
    echo "Build failed: binary not found at $BINARY"
    exit 1
fi

chmod +x "$BINARY"

echo
echo "Done. Linux executable: $BINARY"
echo "Built against glibc 2.35 (Ubuntu 22.04) -- should run on Ubuntu 22.04 and newer."
