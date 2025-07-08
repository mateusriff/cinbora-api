from python:3.12.3-slim

WORKDIR /src

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /src/requirements.txt

RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /src