# ScoutOSAI

ScoutOSAI is split into a FastAPI backend and a React frontend. Docker Compose sets up the backend and a PostgreSQL database.

## Getting Started

### Backend
1. Install dependencies:
   ```bash
   cd scoutos-backend
   pip install -r requirements.txt
   ```
2. Start the API:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend
1. Install packages:
   ```bash
   cd scoutos-frontend
   npm install
   ```
2. Start the dev server:
   ```bash
   npm run dev
   ```
   Visit the app at `http://localhost:5173` by default.

### Docker Compose
Alternatively start both backend and database using Docker:
```bash
docker-compose up
```

## Running Tests

### Backend Tests
Tests use `pytest`. After installing dev dependencies, run:
```bash
cd scoutos-backend
pytest
```

### Frontend Tests
If you add tests using a framework like Jest or Vitest, run:
```bash
cd scoutos-frontend
npm test
```
