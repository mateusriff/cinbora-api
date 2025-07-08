# CInBora

REST API for a college project.

## Dependencies

- Docker
- Python 3.12.3 (use a venv)

## Setup

First setup the repo using:
```bash
$ chmod +x ./setup.sh
$ sudo ./setup.sh
```

## Running App

With Docker installed, make sure you are in the "compose" folder and run the compose command:
```bash
$ cd compose
$ docker compose up --build
```

Observe that 4 services goes up:

1. [App](http://localhost:8000/docs)
2. [Test-DB](http://localhost:5432) (_use a database manager_)
3. [Prometheus](http://localhost:9090)
4. [Grafana](http://localhost:3000)

All of them should be accessible in your _localhost_ or _127.0.0.1_.
