# Backend

FastAPI service for Super Inspections.

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Frontend

The app serves the built frontend (`static/`) at `/` via `app.frontend()` in `app/main.py`.
Run `npm run build` in `../frontend` to (re)generate it; the Vite config outputs directly into
`backend/static`, so it lives inside this deploy directory. Without it, only the API routes
(`/health`, `/inspections`, `/docs`) respond.

FastAPI Cloud only builds Python projects — it does not run `npm run build`. Before deploying,
build the frontend locally (or in CI) and commit `backend/static/` so it's present in the deploy.