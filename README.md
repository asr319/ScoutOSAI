# ScoutOSAI

ScoutOSAI provides a simple agent platform split into two parts: a FastAPI backend and a React frontend. Docker Compose bundles the backend with a PostgreSQL database. Each subdirectory includes additional documentation.

## Setup

Run the setup script to install all dependencies:

```bash
./setup.sh
```

The script installs Python packages for `scoutos-backend` and Node packages for `scoutos-frontend`. You can also install them manually:

```bash
cd scoutos-backend && pip install -r requirements.txt -r requirements-dev.txt
cd ../scoutos-frontend && pnpm install
```

## Running Tests

### Backend
Execute the unit tests with `pytest` after installing the development requirements:

```bash
cd scoutos-backend
pytest
```

### Frontend
Run the Vitest suite from the frontend directory:

```bash
cd scoutos-frontend
pnpm test
```

## Development

- Start the FastAPI backend:
  ```bash
  uvicorn app.main:app --reload
  ```
- Launch the frontend dev server:
  ```bash
  pnpm --dir scoutos-frontend run dev
  ```

Docker Compose can also start the backend together with PostgreSQL:

```bash
docker-compose up
```

See the `scoutos-backend` and `scoutos-frontend` READMEs for more details.
