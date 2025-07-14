# Backend Guidelines

## Style

- Follow **PEP8** for formatting and code structure.
- Use Python **type hints** for all function signatures and important variables.

## Testing

- Tests rely on **SQLite**. The `conftest.py` in `tests/` sets `DATABASE_URL` to `sqlite:///./test.db` automatically.
- Run tests from the `scoutos-backend` directory with:

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

## CI/CD and Automation Policy

The backend participates in the global `full-checks.yml` workflow. Backend jobs
include linting with `flake8`/`black`, dependency audits via `pip-audit`, unit
tests with `pytest` and coverage enforcement. Static analysis (`bandit`),
dead code checks (`vulture`), license validation, and container image scanning are also run.
Commit and PR messages must state `All CI/CD, security, and agent checks passed.` Failures trigger the Codex Agent to attempt auto-fixes before re-running the workflow.
Keep this AGENTS file aligned with project policies. Record updates in `logs/agents.log`.
