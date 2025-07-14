# ScoutOSAI

## Setup

`docker-compose.yml` expects the database password in `POSTGRES_PASSWORD`, an
OpenAI API key in `OPENAI_API_KEY`, and two encryption keys: `FERNET_KEY` and
`APP_ENCRYPTION_KEY`. Generate each key with `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
and set the variables before starting the stack:

```bash
export POSTGRES_PASSWORD=yourpassword
export OPENAI_API_KEY=sk-...
export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
export APP_ENCRYPTION_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
export OPENAI_API_KEY=sk-...
docker-compose up
```

Sample environment files are provided for development, staging, and production.
Copy the appropriate file to `.env` and pass it to docker-compose:

```bash
cp .env.staging.example .env  # or .env.prod.example
docker-compose --env-file .env up
```

The backend service uses these values when constructing `DATABASE_URL` and when
calling the OpenAI API for the demo AI endpoints.

The compose file also builds the React frontend so the full stack runs with a
single command. Visit `http://localhost:3000` after running `docker-compose up`.

ScoutOSAI is a demo full-stack project that pairs a FastAPI backend with a React + Vite frontend. The application exposes a small API for managing user information and storing short text "memories". The web client provides a minimal chat interface for experimenting with the API.

## Backend Setup

The backend lives in [`scoutos-backend`](scoutos-backend/). Install dependencies and start the server with:

```bash
cd scoutos-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The service reads `DATABASE_URL` to connect to PostgreSQL (tests override this with SQLite). Set both `FERNET_KEY` and `APP_ENCRYPTION_KEY` to random strings so `Memory.content` can be encrypted. See [`scoutos-backend/README.md`](scoutos-backend/README.md) for more details on environment variables and endpoints.
Additional agent documentation and plugin examples are in [AGENTS.md](AGENTS.md).

Run the backend unit tests from the same directory:

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

### Enabling Two-Factor Authentication

User registration now returns a `totp_secret` value. Scan this key in any TOTP
app (Google Authenticator, Authy, etc.) and provide the generated code when
logging in via `/user/login` using the `totp_code` field.

## Frontend Setup

The React frontend is found in [`scoutos-frontend`](scoutos-frontend/). Use `pnpm` for dependency management:

```bash
cd scoutos-frontend
pnpm install
```

Create a `.env` file with the backend URL:

```
VITE_API_URL=http://localhost:8000
```

Start the development server with:

```bash
pnpm run dev
```

The UI includes a dark mode toggle in the navigation bar. Use it to switch
between light and dark themes.

Lint and run tests with (`pnpm test` starts watch mode):

```bash
npm run lint
pnpm test -- --run
```

## Security Notes

This repository is a learning project. When adapting it for workloads that touch HIPAA or banking data:

- Serve all traffic over **HTTPS** to protect sensitive information in transit.
- Use **strong, unique passwords** and store secrets in environment variables or a secret manager, never in version control.
- Limit CORS origins and employ authentication before exposing the API publicly.

Review [`SECURITY.md`](SECURITY.md) and your organization’s compliance requirements before deploying in production.

## API Reference

Full details of the REST endpoints, including example requests, can be found in
[`scoutos-backend/README.md`](scoutos-backend/README.md).

Additional agent documentation and plugin examples are in [AGENTS.md](AGENTS.md).

## Analytics

Usage events like memory creation and agent calls are stored in an
`analytics_events` table. Two endpoints expose this data:

- `GET /analytics/summary` – return a count of events grouped by type for the
  authenticated user.
- `GET /analytics/events` – return recent events. Pass `?format=csv` to export
  a CSV file instead of JSON.
