⚠️ BekonOS (c) 2025 asr319. All rights reserved. Proprietary License – see LICENSE for terms.
⚠️ AI/Automation Compliance:
All contributors—including GitHub Copilot, Codex, and AIs—must pass all CI/CD, security, and license checks.
See AGENTS.md and workflows for requirements.

# AGENTS instructions

Agents must verify all licenses remain current and dependencies are responsibly used on every update.

Last updated: 2025-07-15
Scan status: All checks passed on 2025-07-15

This frontend uses **pnpm** for dependency management. Run `pnpm install` to install packages.

- Start the Vite development server with `pnpm run dev`.
- Run unit tests with `pnpm test` (watch mode) or `pnpm test -- --run` for a single run.

## License and Dependency Compliance

All third-party packages must use compatible licenses. Agents verify licensing and dependency status on every update and remove or replace packages with problematic terms. Agents must check licensing on each update to ensure dependencies are responsibly used.

## License Compliance Policy

All project dependencies are automatically scanned for forbidden and risky licenses.
Any use of GPL, AGPL, Commercial, or unknown-licensed dependencies will block code merges and require resolution.
Last scan: 2025-07-15 — Status: PASS
See ../../LICENSES-node.md for a current list.

- Run ESLint with `npm run lint`.
- Format all project files with `pnpm exec prettier --write .` and generate `.min.js` and `.min.css` files using Vite or another minifier.
- From the repository root run `python scripts/check_duplicates.py` to detect redundant files and clean them up.
- Frontend logs should be written to `logs/frontend.log` instead of embedded in source files.

## CI/CD and Automation Policy

Frontend checks run as part of `full-checks.yml`. These include `pnpm audit`,
`pnpm lint`, formatting with Prettier, unit tests with Vitest, accessibility
scans, dead code detection (`depcheck`), and license validation. Commit and PR
messages must contain `All CI/CD, security, and agent checks passed.` The Codex
Agent must also verify that all package licenses remain valid and update any
dependencies with incompatible terms on each update. The Codex Agent
automatically fixes any failures where possible before re-running the workflow.
Keep this AGENTS file updated with workflow changes. Record modifications in `logs/agents.log`.

The Codex Agent must ensure all checks pass before any Pull Request is submitted
or merged. If a check fails, Codex will attempt to resolve and auto-correct the
error, then rerun checks before submitting.

## Agent Contracts and Validation

Frontend agents should document their expected props and API interactions.
Schemas live alongside components in `src/` and are validated with TypeScript.
The `scripts/validate_agents.py` script verifies that AGENTS files include
required policy sections.

## BekonOS Brand Kit

Use assets/bekonos-logo.svg in UI and docs. Primary color #1C7CF6, accent #FFC857. Headlines use Montserrat; body uses Inter. Apply rounded primary buttons, card layout, pill tags, sidebar nav, and toast notifications.
