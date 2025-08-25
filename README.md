This is a [FastAPI](https://fastapi.tiangolo.com/) project bootstrapped with [`Poetry`](https://python-poetry.org/).

## Getting Started

First, make sure that you have an updated version of `Poetry`:

```bash
poetry self update
```

Also, make sure you're using at least `Python` 3.13

To install the dependencies, run:

```bash
poetry install
```

Then, run the development server:

```bash
poetry run uvicorn main:app --reload
```

The API will be server on [http://localhost:8000](http://localhost:8000).
