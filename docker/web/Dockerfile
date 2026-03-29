FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y gettext \
    && rm -rf /var/lib/apt/lists/*

COPY requirements /app/requirements

RUN pip install --upgrade pip \
    && pip install -r /app/requirements/local.txt

COPY . /app

RUN chmod +x /app/docker/web/entrypoint.sh

WORKDIR /app/src

