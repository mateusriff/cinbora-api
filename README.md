# CInBora

REST API for a college project.

## Dependencies

- Docker
- Python 3.12.3 (use a venv)

## Setup

First setup the repo using:
1. Ubuntu:
```bash
$ chmod +x ./setup.sh
$ sudo ./setup.sh
```

2. Windows:
```powershell
> .\setup.bat
```

## Enviroment Variables

You will need to create a file named **.env** inside the folder **compose**:

```python
POSTGRES_USER=meuusuario
POSTGRES_PASSWORD=senhasecreta
POSTGRES_DB=meubanco
POSTGRES_HOST=db
POSTGRES_PORT=5432
AWS_DEFAULT_REGION=
AWS_COGNITO_SECRET_NAME=
BUCKET_NAME=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_SESSION_TOKEN=
```

Contact **pass@cin.ufpe.br** or **bor@cin.ufpe.br** to get access to AWS enviroment variables and tokens.

## Running App

With Docker installed, make sure you are in the "compose" folder and run the compose command:
```bash
$ cd compose
$ docker compose up --build
```

Observe that 2 services goes up:

1. [App](http://localhost:8000/docs)
2. [Test-DB](http://localhost:5432) (_use a database manager_)

All of them should be accessible in your _localhost_ or _127.0.0.1_.
