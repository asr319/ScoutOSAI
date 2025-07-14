# AGENTS instructions
Last updated: 2025-07-14

This frontend uses **pnpm** for dependency management. Run `pnpm install` to install packages.

- Start the Vite development server with `pnpm run dev`.
- Run unit tests with `pnpm test` (watch mode) or `pnpm test -- --run` for a single run.
- Run ESLint with `npm run lint`.
- Format all project files with `pnpm exec prettier --write .` and generate `.min.js` and `.min.css` files using Vite or another minifier.
- From the repository root run `python scripts/check_duplicates.py` to detect redundant files and clean them up.
- Frontend logs should be written to `logs/frontend.log` instead of embedded in source files.

## CI/CD and Automation Policy

Frontend checks run as part of `full-checks.yml`. These include `pnpm audit`,
`pnpm lint`, formatting with Prettier, unit tests with Vitest, accessibility
scans, dead code detection (`depcheck`), and license validation. Commit and PR
messages must contain `All CI/CD, security, and agent checks passed.` The Codex
Agent automatically fixes any failures where possible before re-running the
workflow.
Keep this AGENTS file updated with workflow changes. Record modifications in `logs/agents.log`.

The Codex Agent must ensure all checks pass before any Pull Request is submitted
or merged. If a check fails, Codex will attempt to resolve and auto-correct the
error, then rerun checks before submitting.

## Agent Contracts and Validation

Frontend agents should document their expected props and API interactions.
Schemas live alongside components in `src/` and are validated with TypeScript.
The `scripts/validate_agents.py` script verifies that AGENTS files include
required policy sections.
