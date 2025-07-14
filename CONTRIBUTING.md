# Contributing to ScoutOSAI

Thank you for contributing! ScoutOSAI enforces automated CI/CD and security workflows for all changes. Before opening a Pull Request, ensure the following:

1. Run the full test and lint suite locally (`pnpm lint`, `pnpm test`, `flake8`, `black`, `pytest`).
2. Run `prettier --write .` and generate `.min.js`/`.min.css` assets as needed.
3. Update `CHANGELOG.md` and bump the project version when appropriate.
4. Verify no secrets or sensitive data are committed (`python scripts/scan_for_secrets.py`).
5. Document any new agents or endpoints in the relevant `AGENTS.md` file.
6. Commit messages and PR descriptions must include:
   `All CI/CD, security, and agent checks passed.`
7. The GitHub Actions workflow `full-checks.yml` must succeed before merge. This workflow performs secret scanning, vulnerability audits, linting, formatting, tests, static analysis, license checks, coverage enforcement, accessibility scans, and more. It also validates all `AGENTS.md` files.
8. If a job fails, fix the issue and push updates. The Codex Agent will attempt automatic formatting or dependency updates and then rerun the workflow.
