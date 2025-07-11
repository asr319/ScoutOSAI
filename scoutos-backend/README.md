# ScoutOSAI Backend

This directory contains the FastAPI service.  It exposes a small set of endpoints
for user and memory management.

## Installation

```bash
pip install -r requirements.txt
cp .env.example .env  # configure DATABASE_URL if needed
```

## Development

Run the API locally with

```bash
uvicorn app.main:app --reload
```

The service reads the `DATABASE_URL` environment variable to connect to
PostgreSQL.

## API Endpoints

| Method | Path          | Description               |
| ------ | ------------- | ------------------------- |
| `GET`  | `/`           | Health check              |
| `POST` | `/memory/add` | Store a memory (demo)     |
| `POST` | `/user/create`| Create a user (demo)      |
| `GET`  | `/agent/status`| Agent status placeholder |

## Deployment

The provided `Dockerfile` can be deployed on platforms such as Railway or
Fly.io.  Ensure that `DATABASE_URL` and any other secrets are configured in the
host environment.

## Tests

Install the development requirements before running the unit tests:

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

Contributions are welcome!  See the repository root `README.md` for more
information.
