<!-- @format -->

# ScoutOSAI

ScoutOSAI is a small full‑stack example for building an AI agent with long term memory. The repository contains a FastAPI backend and a React/Vite frontend. The backend exposes endpoints for user accounts and storing or merging "memories" in a PostgreSQL database while the frontend provides a simple chat style interface.

## Getting Started

Use the provided `setup.sh` script to install all backend and frontend dependencies. It will install Python packages for the API and `pnpm` packages for the web client.

```bash
./setup.sh
```

### Running the Backend

The API lives in `scoutos-backend`. After installing dependencies you can start a development server with:

```bash
cd scoutos-backend
uvicorn app.main:app --reload
```

`DATABASE_URL` should point at your PostgreSQL instance. During early development all CORS origins are allowed.

Backend tests are executed with `pytest`:

```bash
pytest
```

### Running the Frontend

The web client resides in `scoutos-frontend`. Create a `.env` file with the backend URL:

```
VITE_API_URL=http://localhost:8000
```

Then launch the dev server:

```bash
cd scoutos-frontend
pnpm run dev
```

Run the frontend test suite with:

```bash
npm test
```

## Repository Layout

- `scoutos-backend` – FastAPI service with memory and user endpoints
- `scoutos-frontend` – React/Vite app communicating with the API
- `setup.sh` – helper script to install all project dependencies

Both projects include additional README files with further details.

