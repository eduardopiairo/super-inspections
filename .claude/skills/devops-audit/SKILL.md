---
name: devops-audit
description: Run the DevOps/CI-CD best-practices audit for this repo, walk through the manual checks, and update docs/devops-checklist.md. Use before releases, after changing pipelines or repo settings, or when asked to validate DevOps practices.
---

# DevOps audit

Source of truth for the checks is `scripts/audit-devops.sh` and `docs/devops-checklist.md`. Do not
re-implement checks here; if a check is missing, add it to the script and the checklist.

## Rules
- Read-only by default. Never change GitHub, Netlify, Neon or FastAPI Cloud settings, secrets or branch
  protection without the user confirming that specific action first.
- Never ask for, print or handle secret values. Only check that a secret exists by name.

## Steps
1. Run `scripts/audit-devops.sh` from the repo root. It needs `gh` (logged in) and `jq`. If it can't run,
   say why and stop.
2. Group the output: FAIL first, then SKIP, then PASS counts. For each FAIL give the fix in one line
   (the exact `gh api` command or the settings page), and mark it as a write that needs confirmation.
3. Ask the user about each manual check the script lists and record the answer:
   - Netlify Git auto-build is off
   - Neon backups / point-in-time restore on, app uses a non-owner role
   - FastAPI Cloud `DATABASE_URL` and `CORS_ORIGINS` set
   - Rollback tried once (Netlify, FastAPI Cloud, Neon)
   - Each clone ran `pre-commit install` (gitleaks)
   Mark an item ❓ if the user doesn't know.
4. Update the status column in `docs/devops-checklist.md` (✅ / ❌ / ❓) and the date in its intro, using
   the audit output and the user's answers as evidence. Change statuses only; do not reword rows.
5. Finish with a short summary: counts of pass/fail/unknown, the top 3 fixes by impact, and which
   changes need the user's confirmation. Do not commit unless asked.
