⚠️ BekonOS (c) 2025 asr319. All rights reserved. Proprietary License – see LICENSE for terms.
⚠️ AI/Automation Compliance:

All contributors—including GitHub Copilot, Codex, and AIs—must pass all CI/CD, security, and license checks.

<p align="center">
  <img src="./assets/bekonos-logo.svg" alt="BekonOS Logo" width="340"><br>
  <strong>BekonOS&nbsp;<sup>©</sup></strong>
</p>

See AGENTS.md and workflows for requirements.
Last updated: 2025-07-15
Scan status: All checks passed on 2025-07-15

# BekonOS

Lost in Data’s Sway? BekonOS Saves the Day!

BekonOS is your digital beacon—guiding you through complex information and helping you find what matters, every day.

## Setup

`docker-compose.yml` expects the database password in `POSTGRES_PASSWORD`, an
OpenAI API key in `OPENAI_API_KEY`, a JWT `SECRET_KEY`, and two encryption keys:
`FERNET_KEY` and `APP_ENCRYPTION_KEY`. Generate each key with
`python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
and set the variables before starting the stack:

```bash
export POSTGRES_PASSWORD=yourpassword
export OPENAI_API_KEY=sk-...
export SECRET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
export APP_ENCRYPTION_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
docker-compose up
```

Sample environment files are provided for development, staging, and production.
Copy the appropriate file to `.env` and pass it to docker-compose:

```bash
cp .env.staging.example .env  # or .env.prod.example
docker-compose --env-file .env up
```

### Environment Variables

BekonOS relies on several environment variables for configuration:

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` – PostgreSQL credentials.
- `DATABASE_URL` – connection string used by the backend.
- `OPENAI_API_KEY` – key for the OpenAI API.
- `FERNET_KEY` and `APP_ENCRYPTION_KEY` – encryption keys for stored data.
- `SECRET_KEY` – signing key for JWT tokens.
- `ALLOWED_ORIGINS` – comma-separated CORS origins.
- `AGENT_BACKEND` – set to `local` to disable OpenAI calls.
- `VITE_API_URL` – URL to the backend API.
- `VITE_USE_MOCK` or `VITE_USE_MOCK_AI` – enable the mock API during local development.
- `VITE_ENV` – build environment identifier (`development` or `production`).
- `SCOUTOS_CUSTOM_DOMAIN` – domain name for GitHub Pages or local testing.
- `SCOUTOS_ALLOWED_DOMAINS` – comma-separated list of allowed hosts for network calls.

Sample `.env` files include these variables with placeholder values.

The backend service uses these values when constructing `DATABASE_URL` and when
calling the OpenAI API for the demo AI endpoints.

The compose file also builds the React frontend so the full stack runs with a
single command. Visit `http://localhost:3000` after running `docker-compose up`.

### Offline / Mock Mode

To develop completely offline set `AGENT_BACKEND=local` (or `MOCK_AI=true`) for
the backend and `VITE_USE_MOCK=true` in `scoutos-frontend/.env`. Mock mode
returns canned responses so you can explore the UI without network access or API
keys.

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

Copy `scoutos-frontend/.env.example` to `.env` and adjust as needed:

```
VITE_API_URL=http://localhost:8000
VITE_ENV=development
VITE_USE_MOCK_AI=true
VITE_USE_MOCK=true
SCOUTOS_CUSTOM_DOMAIN=dev.scoutos.local
SCOUTOS_ALLOWED_DOMAINS=localhost,127.0.0.1,scoutos.local,asr319.github.io,dev.scoutos.local,api.openai.com,registry.npmjs.org,pypi.org,pnpm.io,vitest.dev,github.com,files.pythonhosted.org
```

Start the development server with:

```bash
pnpm run dev
```

The UI includes a dark mode toggle in the navigation bar. Use it to switch
between light and dark themes.

Lint and run tests with:

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

### Secret Scanning

All pushes and pull requests to `main` or `develop` run [Gitleaks](https://github.com/zricethezav/gitleaks) to detect hardcoded secrets. Run `python scripts/scan_for_secrets.py` locally to scan your working tree. Add additional patterns in the `SECRET_PATTERNS` list if needed.

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

## License and Dependency Compliance

All third-party packages must use compatible licenses. Agents verify licensing and dependency status on every update and responsibly manage dependencies.

## License Compliance Policy

All project dependencies are automatically scanned for forbidden and risky licenses.
Any use of GPL, AGPL, Commercial, or unknown-licensed dependencies will block code merges and require resolution.
Last scan: 2025-07-15 — Status: PASS
See LICENSES-python.md and LICENSES-node.md for a current, full list.

## License

Proprietary – BekonOS (c) 2025 asr319. All rights reserved. No use, copying, or redistribution without permission. Some dependencies under open source licenses; see NOTICE.txt for details.

## BekonOS Brand Kit

- Logo: assets/bekonos-logo.svg
- Colors: Beacon Blue #1C7CF6, Signal Yellow #FFC857, Background #E9EEF6/#FFFFFF, Dark #181E29
- Fonts: Montserrat headlines, Inter body
- UI components: dashboard layout, rounded primary buttons, cards, timeline UI, pill tags, sidebar navigation, toasts
