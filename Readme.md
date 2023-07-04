# FastAPI file server
This is a demo app showcasing a simple file server written in FastAPI

## Installing
First, install all dependencies (using `pip`).


```shell
python3 -m venv .venv      # skip if you don't need a virtual env
source .venv/bin/activate  # skip if you don't need a virtual env

pip install -r requirements.txt  # install dependencies
```

## Starting the server
This is just a demo, start the server in development mode.

```shell
uvicorn main:app --reload  # start server with autoreload (dev mode)
```

Starting the server exposes:
* Swagger at `http://127.0.0.1:8000/docs/
* API at `http://127.0.0.1:8000`

The API documentation is available in Swagger.

## Authentication
Authentication is not implemented.
