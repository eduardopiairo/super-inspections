# Frontend

Vite-based JS frontend for Super Inspections. In production, the built output is served directly
by the FastAPI backend via `app.frontend()` (see `backend/app/main.py`) — there is no separate
frontend deploy or `pyproject.toml` here, since this isn't a Python project.

The build outputs into `../backend/static` (not `dist/`) so it lands inside the backend's deploy
directory for FastAPI Cloud.

## Setup

```bash
cd frontend
npm install
```

## Run (dev)

```bash
npm run dev
```

Requests to backend routes (`/health`, `/inspections`) are proxied to `http://localhost:8000`
during development (see `vite.config.js`), so run `fastapi dev` in `backend/` alongside this.

## Build

```bash
npm run build
```

This outputs to `backend/static/`, which the backend serves at `/` when running from `backend/`.
Commit `backend/static/` before deploying to FastAPI Cloud — it does not run this build step.
