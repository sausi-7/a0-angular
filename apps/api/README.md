# apps/api — FastAPI backend

## Run locally

```bash
cd apps/api
uv sync --all-extras --dev
uv run uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`.

## Run tests

```bash
uv run pytest -q
```

## Lint / typecheck

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

## Layout

```
app/
  main.py        # FastAPI app and routes
  config.py      # Pydantic settings (env-driven)
tests/           # pytest
pyproject.toml   # uv-managed deps
```

Phase 0 scope: health endpoint only. Phase 1 adds project CRUD and the agent WebSocket.
