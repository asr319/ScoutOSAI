⚠️ BekonOS (c) 2025 asr319. All rights reserved. Proprietary License – see LICENSE for terms.
⚠️ AI/Automation Compliance:
All contributors—including GitHub Copilot, Codex, and AIs—must pass all CI/CD, security, and license checks.
See AGENTS.md and workflows for requirements.
Last updated: 2025-07-15
Scan status: All checks passed on 2025-07-15

# BekonOS Frontend

Lost in Data’s Sway? BekonOS Saves the Day!

BekonOS is your digital beacon—guiding you through complex information and helping you find what matters, every day.

This directory contains the React + Vite web client. The UI communicates with
the backend API and provides a simple chat interface.

## Setup

```bash
pnpm install
```

During development the app expects several environment variables. Copy
`.env.example` to `.env` and adjust as needed:

```
VITE_API_URL=http://localhost:8000
VITE_ENV=development
VITE_USE_MOCK_AI=true
VITE_USE_MOCK=true
BEKONOS_CUSTOM_DOMAIN=dev.bekonos.local
BEKONOS_ALLOWED_DOMAINS=localhost,127.0.0.1,scoutos.local,asr319.github.io,dev.bekonos.local,api.openai.com,registry.npmjs.org,pypi.org,pnpm.io,vitest.dev,github.com,files.pythonhosted.org
```

Run the development server with

```bash
pnpm run dev
```

## Deployment

The built site is static and can be deployed on Vercel, Netlify or Railway.
Ensure the `VITE_API_URL` environment variable points to your deployed backend.

Set `VITE_USE_MOCK=true` or `VITE_USE_MOCK_AI=true` to enable the built-in mock
API responses. This allows the UI to run without a backend during development or
testing.

## Linting and Tests

`npm run lint` will run ESLint.

### Running Tests

Tests are written with [Vitest](https://vitest.dev). Execute them with:

```bash
npm test
```

Contributions are welcome!

## Mobile Installation

The frontend can be installed as a Progressive Web App. After running `pnpm run build` and serving the `dist` folder, visit the site on a mobile browser and choose **Add to Home Screen**. The layout is responsive and adapts to small screens through Tailwind CSS.

## License and Dependency Compliance

All third-party packages must use compatible licenses. Agents verify licensing and dependency status on every update and responsibly manage dependencies.

## License

Proprietary – BekonOS (c) 2025 asr319. All rights reserved. No use, copying, or redistribution without permission. Some dependencies under open source licenses; see ../../NOTICE.txt for details.
