# syntax=docker.io/docker/dockerfile:1

FROM astral/uv:python3.14-bookworm-slim

WORKDIR /usr/src/app

# Enable bytecode compilation to improve startup time (at the cost of increased installation time).
ENV UV_COMPILE_BYTECODE=1

# Install directly to system Python instead of into a virtual environment, as a container image (per definition) is
# already isolated.
ENV UV_SYSTEM_PYTHON=1

COPY requirements.txt ./
RUN uv pip install --no-cache-dir -r requirements.txt

# Include only the source code.
COPY ./src .

ENTRYPOINT [ "python", "hatch_python_project_template/main.py" ]

LABEL name="hatch-python-project-template"
LABEL maintainer="https://github.com/h-holm"
LABEL description="A template Python project"
LABEL url="https://github.com/h-holm/hatch-python-project-template"
