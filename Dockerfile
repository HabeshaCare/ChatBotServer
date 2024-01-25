# syntax=docker/dockerfile:1

FROM python:3.10.13-slim-bookworm

WORKDIR /python-docker

# Install a C++ compiler with C++11 support (g++) and other required tools
RUN apt-get update && apt-get install -y g++ && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "-c", "gunicorn.conf.py"]
