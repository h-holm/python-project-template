# syntax=docker.io/docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /usr/src/app

# Install `git` and `pipx` (in order to install Hatch). Remember to delete the `apt` cache to reduce the
# image size.
RUN apt-get update && apt-get install -y \
    git \
    pipx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Hatch via `pipx`.
RUN pipx install hatch

# Set the locale.
ENV LC_ALL=C

# Add `/root/.local/bin` to `$PATH` to ensure Hatch can be detected.
ENV PATH="$PATH:/root/.local/bin"
