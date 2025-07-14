# ScoutOSAI Backend

This directory contains the FastAPI service. It exposes a small set of endpoints
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

When running via Docker, auto-reload can be enabled by setting the
`UVICORN_RELOAD` environment variable:

```bash
docker run -e UVICORN_RELOAD="--reload" your-image
```

The service reads the `DATABASE_URL` environment variable to connect to
PostgreSQL. The backend uses SQLAlchemy's **sync** engine so the URL must
use the standard `postgresql://` scheme (not the `postgresql+asyncpg://`
variant). Allowed CORS origins are configured with the `ALLOWED_ORIGINS`
environment variable. Provide a comma–separated list of origins; by default `*`
is used to allow all origins during development. Set `OPENAI_API_KEY` so the AI
demo endpoints can call the OpenAI API.

### Environment variables

Database credentials and your OpenAI key, API keys and encryption keys are provided via a `.env` file. From the repository root,
copy `.env.example` to `.env` and adjust the values as needed:

```bash
cp .env.example .env
```

Generate random base64 values for `FERNET_KEY` and `APP_ENCRYPTION_KEY` with:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Docker Compose reads this file automatically when launching the services.

Important variables include:

- `SECRET_KEY` – JWT signing key.
- `ALLOWED_ORIGINS` – comma-separated list for CORS.
- `DATABASE_URL` – PostgreSQL connection string.
- `OPENAI_API_KEY` – OpenAI credentials.
- `FERNET_KEY` and `APP_ENCRYPTION_KEY` – data encryption keys.
- `AGENT_BACKEND` or `MOCK_AI` – set to `local` or `true` to disable OpenAI calls.

The `LocalBackend` returns stubbed responses so you can run the API without network
access or API keys.

## API Endpoints

The service exposes a small REST API. The table below lists each route and its
purpose.

| Method   | Path                  | Description                       |
| -------- | --------------------- | --------------------------------- |
| `GET`    | `/`                   | Health check                      |
| `POST`   | `/user/register`      | Register a user                   |
| `POST`   | `/user/login`         | Obtain auth token (TOTP required) |
| `GET`    | `/user/profile`       | Get user profile                  |
| `PUT`    | `/user/profile`       | Update user profile               |
| `GET`    | `/agent/status`       | Agent status placeholder          |
| `POST`   | `/agent/merge`        | Merge multiple memories           |
| `POST`   | `/memory/add`         | Store a memory                    |
| `PUT`    | `/memory/update/{id}` | Update a memory                   |
| `GET`    | `/memory/list`        | List memories for a user          |
| `GET`    | `/memory/search`      | Filter by topic, tag, or content  |
| `DELETE` | `/memory/delete/{id}` | Delete a memory                   |
| `POST`   | `/ai/chat`            | Chat with OpenAI                  |
| `POST`   | `/ai/tags`            | Suggest tags for text             |
| `POST`   | `/ai/merge`           | LLM merge advice                  |
| `POST`   | `/ai/summary`         | Summarize text                    |
| `GET`    | `/analytics`          | Admin only usage stats            |

Authenticate via `/user/login` to obtain a JWT `token`. Pass this token in the
`Authorization` header as `Bearer <token>` when calling any `/memory` or `/agent`
route.

### Two-Factor Authentication

`/user/register` returns a `totp_secret` key for the newly created account.
Add this secret to an authenticator app and pass the current TOTP code as
`totp_code` when calling `/user/login`.

### Example Requests

**Add a memory**

```http
POST /memory/add HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": 1,
  "content": "Buy milk",
  "topic": "todo",
  "tags": ["grocery"]
}
```

Response

```json
{
  "message": "Memory added",
  "memory": {
    "id": 42,
    "user_id": 1,
    "content": "Buy milk",
    "topic": "todo",
    "tags": ["grocery"]
  }
}
```

**List memories**

```http
GET /memory/list?user_id=1 HTTP/1.1
Authorization: Bearer <token>
```

Response

```json
[
  {
    "id": 42,
    "user_id": 1,
    "content": "Buy milk",
    "topic": "todo",
    "tags": ["grocery"]
  }
]
```

**Delete a memory**

```http
DELETE /memory/delete/42?user_id=1 HTTP/1.1
Authorization: Bearer <token>
```

Response

```json
{ "message": "Memory deleted" }
```

**AI chat**

```http
POST /ai/chat HTTP/1.1
Content-Type: application/json

{"prompt": "Hello"}
```

Response

```json
{ "response": "Hi there!" }
```

## Deployment

The provided `Dockerfile` can be deployed on platforms such as Railway or
Fly.io. Ensure that `DATABASE_URL` and any other secrets are configured in the
host environment.

## Tests

Install the development requirements before running the unit tests:

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

Contributions are welcome! See the repository root `README.md` for more
information.
