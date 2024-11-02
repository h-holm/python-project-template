# syntax=docker.io/docker/dockerfile:1

FROM python:3.13-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./

ENTRYPOINT [ "python", "./python_project/main.py" ]

LABEL name="python-project"
LABEL maintainer="no-reply@email.com"
LABEL description="A template Python project"
LABEL url="https://github.com/h-holm/python-project"
