# ScoutOSAI Frontend

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
SCOUTOS_CUSTOM_DOMAIN=dev.scoutos.local
SCOUTOS_ALLOWED_DOMAINS=localhost,127.0.0.1,scoutos.local,asr319.github.io,dev.scoutos.local,api.openai.com,registry.npmjs.org,pypi.org,pnpm.io,vitest.dev,github.com,files.pythonhosted.org
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
