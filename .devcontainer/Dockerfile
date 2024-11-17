# syntax=docker.io/docker/dockerfile:1

FROM python:3.13-alpine

WORKDIR /usr/src/app

# Install `git`.
RUN apk add --no-cache git

# Install `pipx` in order to install Hatch.
RUN apk add --no-cache pipx
RUN pipx ensurepath --global

# Install Hatch via `pipx`.
RUN pipx install hatch

# Add `/root/.local/bin` to `$PATH` to ensure Hatch can be detected.
ENV PATH="$PATH:/root/.local/bin"
