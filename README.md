# ScoutOSAI

## Setup

`docker-compose.yml` expects the database password in the `POSTGRES_PASSWORD`
environment variable. Set the variable before starting the stack:

```bash
export POSTGRES_PASSWORD=yourpassword
docker-compose up
```

The backend service uses this value when constructing `DATABASE_URL`.

ScoutOSAI is a demo full-stack project that pairs a FastAPI backend with a React + Vite frontend. The application exposes a small API for managing user information and storing short text "memories". The web client provides a minimal chat interface for experimenting with the API.

## Backend Setup

The backend lives in [`scoutos-backend`](scoutos-backend/). Install dependencies and start the server with:

```bash
cd scoutos-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The service reads `DATABASE_URL` to connect to PostgreSQL (tests override this with SQLite). See [`scoutos-backend/README.md`](scoutos-backend/README.md) for more details on environment variables and endpoints.

Run the backend unit tests from the same directory:

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

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

Lint and run tests with:

```bash
npm run lint
pnpm test
```

## Security Notes

This repository is a learning project. When adapting it for workloads that touch HIPAA or banking data:

- Serve all traffic over **HTTPS** to protect sensitive information in transit.
- Use **strong, unique passwords** and store secrets in environment variables or a secret manager, never in version control.
- Limit CORS origins and employ authentication before exposing the API publicly.

Review [`SECURITY.md`](SECURITY.md) and your organization’s compliance requirements before deploying in production.
