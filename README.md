# ScoutOSAI

ScoutOSAI is split into a FastAPI backend and a React frontend. Docker Compose sets up the backend and a PostgreSQL database.  This repository also contains basic CI and deployment instructions for hosting the project in the cloud.  Each subdirectory contains its own README with additional details.

## Getting Started

Run the setup script to install backend and frontend dependencies:

```bash
./setup.sh
```


### Backend
1. Install dependencies:
   ```bash
   cd scoutos-backend
   pip install -r requirements.txt
   ```
2. Set your OpenAI API key as an environment variable before running the app:
   ```bash
   export OPENAI_API_KEY=<your-key>
   ```
3. *(Optional)* Set `ALLOWED_ORIGINS` with a comma-separated list of allowed
   origins for CORS. The default is `http://localhost:5173`.
4. Start the API:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.
   The backend exposes an `/ai/chat` endpoint which proxies requests to OpenAI.

### Frontend
1. Install packages:
   ```bash
   cd scoutos-frontend
   npm install
   ```
   Copy `.env.example` to `.env` and update the API URL if needed:
   ```bash
   cp .env.example .env
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

## Deployment

The backend is packaged in a Dockerfile and can be deployed to platforms such as
Railway or Fly.io.  The frontend can be deployed to Vercel or Netlify.

1. Build and push the backend image, setting the `DATABASE_URL` and `OPENAI_API_KEY`
   environment variables in your hosting provider.
2. Deploy the `scoutos-frontend` directory as a static site.  Set the
   environment variable `VITE_API_URL` to the public URL of the backend API.

Basic CI is configured using GitHub Actions and runs backend tests on each pull
request.

## Running Tests

### Backend Tests
Tests use `pytest`. After installing dev dependencies, run:
```bash
cd scoutos-backend
python -m pytest
```

### Frontend Tests
If you add tests using a framework like Jest or Vitest, run:
```bash
cd scoutos-frontend
npm test
```
## Contributing
Pull requests are welcome. Please run tests before submitting.



