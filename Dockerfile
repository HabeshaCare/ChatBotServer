# syntax=docker/dockerfile:1

FROM python:3.11
WORKDIR /python-docker

# Install a C++ compiler with C++11 support (g++) and other required tools
RUN apt-get update && apt-get install -y g++ && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y python3-pip
RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.2

COPY . .

RUN poetry install

CMD ["gunicorn", "-c", "gunicorn.conf.py"]
