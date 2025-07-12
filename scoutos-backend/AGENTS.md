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

```bash
uvicorn app.main:app --reload
```
