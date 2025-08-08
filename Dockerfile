from python:3.12.3-slim

WORKDIR /src

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

RUN apt-get update && \
    apt-get install -y awscli build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /src/requirements.txt

RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /src