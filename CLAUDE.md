# Super Inspections

- Monorepo: `backend/` (FastAPI, deployed to FastAPI Cloud), `frontend/` (Vite, deployed to Netlify), Neon Postgres.
- Pipelines: `.github/workflows/`. Overview in `docs/cicd-pipeline.md`.
- Run the `devops-audit` skill before releases and after changing a workflow or repo settings.
  Checklist: `docs/devops-checklist.md`; script: `scripts/audit-devops.sh`.
