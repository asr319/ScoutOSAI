⚠️ BekonOS (c) 2025 asr319. All rights reserved. Proprietary License – see LICENSE for terms.
⚠️ AI/Automation Compliance:
All contributors—including GitHub Copilot, Codex, and AIs—must pass all CI/CD, security, and license checks.
See AGENTS.md and workflows for requirements.

# Backend Guidelines

Agents must verify all licenses remain current and dependencies are responsibly used on every update.

Last updated: 2025-07-15
Scan status: All checks passed on 2025-07-15

## Style

- Follow **PEP8** for formatting and code structure.
- Use Python **type hints** for all function signatures and important variables.

## License and Dependency Compliance

All third-party packages must use compatible licenses. Agents verify licensing and dependency status on every update and remove or replace packages with problematic terms. Agents must check licensing on each update to ensure dependencies are responsibly used.

## License Compliance Policy

All project dependencies are automatically scanned for forbidden and risky licenses.
Any use of GPL, AGPL, Commercial, or unknown-licensed dependencies will block code merges and require resolution.
Last scan: 2025-07-15 — Status: PASS
See ../../LICENSES-python.md for a current list.

## Testing

- Tests rely on **SQLite**. The `conftest.py` in `tests/` sets `DATABASE_URL` to `sqlite:///./test.db` automatically.
- Run tests from the `bekonos-backend` directory with:

```bash
pytest
```

## Local Development

Start the API locally using Uvicorn:

Install dependencies first with `pip install -r requirements.txt -r requirements-dev.txt`.

- From the repository root run `python scripts/check_duplicates.py` to remove any redundant files.
- Backend logs should be written to `logs/backend.log`. Do not keep logs in source files.
- Format all project files with `prettier --write .` and create `.min.js`/`.min.css` assets using a minifier.

```bash
uvicorn app.main:app --reload
```

## Agent Contracts and Validation

Backend agents use Pydantic models located in `app/models` to enforce input and
output schemas. Any new agent must document its schema and add tests. The
`scripts/validate_agents.py` script checks that AGENTS files include required
policy lines.

## CI/CD and Automation Policy

The backend participates in the global `full-checks.yml` workflow. Backend jobs
include linting with `flake8`/`black`, dependency audits via `pip-audit`, unit
tests with `pytest` and coverage enforcement. Static analysis (`bandit`),
dead code checks (`vulture`), license validation, and container image scanning are also run.
Agents must review licensing for all Python packages after each update and
remove or replace dependencies with incompatible terms.
Commit and PR messages must state `All CI/CD, security, and agent checks passed.` Failures trigger the Codex Agent to attempt auto-fixes before re-running the workflow.
Keep this AGENTS file aligned with project policies. Record updates in `logs/agents.log`.

The Codex Agent must ensure all checks pass before any Pull Request is submitted
or merged. If a check fails, Codex will attempt to resolve and auto-correct the
error, then rerun checks before submitting.

## BekonOS Brand Kit

Use assets/bekonos-logo.svg in UI and docs. Primary color #1C7CF6, accent #FFC857. Headlines use Montserrat; body uses Inter. Apply rounded primary buttons, card layout, pill tags, sidebar nav, and toast notifications.
