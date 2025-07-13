# ScoutOSAI Backend

This directory contains the FastAPI service.  It exposes a small set of endpoints
for user and memory management.

## Installation

```bash
pip install -r requirements.txt
```

## Development

Run the API locally with

```bash
uvicorn app.main:app --reload
```

The service reads the `DATABASE_URL` environment variable to connect to
PostgreSQL. The backend uses SQLAlchemy's **sync** engine so the URL must
use the standard `postgresql://` scheme (not the `postgresql+asyncpg://`
variant). Allowed CORS origins are configured with the `ALLOWED_ORIGINS`
environment variable. Provide a comma–separated list of origins; by default `*`
is used to allow all origins during development.  Set `OPENAI_API_KEY` so the AI
demo endpoints can call the OpenAI API.

### Environment variables

Database credentials, API keys and encryption keys are provided via a `.env` file. From the repository root,
copy `.env.example` to `.env` and adjust the values as needed:

```bash
cp .env.example .env
```

Generate random base64 values for `FERNET_KEY` and `APP_ENCRYPTION_KEY` with:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Docker Compose reads this file automatically when launching the services.

## API Endpoints

| Method | Path          | Description               |
| ------ | ------------- | ------------------------- |
| `GET`  | `/`           | Health check              |
| `POST` | `/memory/add` | Store a memory (demo)     |
| `POST` | `/user/register`| Register a user (demo)    |
| `POST` | `/user/login` | Obtain auth token         |
| `GET`  | `/agent/status`| Agent status placeholder |

Authenticate via `/user/login` to receive a `token`. Pass this value in the
`Authorization` header as `Bearer <token>` when calling protected endpoints
like `/memory/update`, `/memory/list`, `/memory/search` or any agent routes.

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
