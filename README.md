<!-- @format -->

# ScoutOSAI

ScoutOSAI is a small demo project that pairs a FastAPI backend with a React
frontend. This document explains how to get a local development environment up
and running and outlines a few security best practices.

## Installation

### Prerequisites

- **Python 3.8+** for the backend
- **Node.js 18+** and [pnpm](https://pnpm.io) for the frontend

Running `./setup.sh` from the repository root will install both Python and
Node.js dependencies using `pip` and `pnpm`.

```bash
./setup.sh
```

### Manual Backend Setup

```bash
cd scoutos-backend
pip install -r requirements.txt -r requirements-dev.txt
```

### Manual Frontend Setup

```bash
cd scoutos-frontend
pnpm install
```

## Configuration

### Backend

The API reads configuration from environment variables:

- `DATABASE_URL` &ndash; PostgreSQL connection string
- `ALLOWED_ORIGINS` &ndash; comma separated list of hosts allowed by CORS

For local development you can start the server with:

```bash
cd scoutos-backend
uvicorn app.main:app --reload
```

### Frontend

Create a `.env` file inside `scoutos-frontend` with the backend URL:

```bash
VITE_API_URL=http://localhost:8000
```

Start the development server using:

```bash
pnpm run dev
```

## Security Guidance

- **Never commit secrets** to the repository. Keep environment variables such as
  database credentials in local `.env` files or the hosting platform's secret
  store.
- Change the default credentials used in `docker-compose.yml` if you expose the
  database outside of local development.
- When deploying, make sure HTTPS is enabled and restrict CORS origins via
  `ALLOWED_ORIGINS`.
- Regularly run `pytest` in `scoutos-backend` and `pnpm test` in
  `scoutos-frontend` to catch regressions.

With these steps you should be able to run both services locally and have a
basic understanding of the security considerations involved.

