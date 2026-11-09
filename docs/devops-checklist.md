# CI/CD best-practices checklist

Use this to review a pipeline change or to audit the repo. Each item is a yes/no question.
The status column reflects the repo as of 2026-11-09. Run `scripts/audit-devops.sh` to re-check the
automated items (see [Validating](#validating-this-checklist)):

- ✅ done
- ❌ not done
- ❓ lives in GitHub, Netlify, Neon or FastAPI Cloud settings, so check it there

Stack: Netlify (frontend), FastAPI Cloud (backend), Neon (Postgres), GitHub Actions (CI/CD).

## 1. Source control and branching

| | Item | Status |
|---|---|---|
| ☐ | `main` is protected: no direct pushes, PR required | ✅ ruleset `protect-default-branch` (repo admins can bypass) |
| ☐ | Required status checks (backend + frontend CI) must pass before merge | ❌ ruleset has no required checks |
| ☐ | At least one review is required, and stale approvals are dismissed on new commits | ✅ 1 approval required; ❌ stale approvals not dismissed |
| ☐ | Force-push and branch deletion are blocked on `main` | ✅ |
| ☐ | Commits are small and focused, and the PR describes what changed and why | ✅ |
| ☐ | `.gitignore` covers `.env`, `node_modules`, `dist`, `.venv` and local DB files | ✅ |

## 2. Continuous integration

| | Item | Status |
|---|---|---|
| ☐ | CI runs on every PR and on pushes to `main` | ✅ |
| ☐ | Path filters keep each pipeline to the code it covers (`backend/**`, `frontend/**`) | ✅ |
| ☐ | Dependencies install from a lockfile (`npm ci`), with caching enabled | ✅ frontend, ❌ backend has no lockfile |
| ☐ | Tests run and fail the build when they fail | ✅ backend, ❌ frontend has no tests yet |
| ☐ | Linting and formatting are enforced (ESLint/Prettier, Ruff) | ❌ |
| ☐ | Type checking is enforced (mypy/pyright) | ❌ |
| ☐ | Test coverage is uploaded to Codecov on every backend run | ✅ workflow, ❌ `CODECOV_TOKEN` not set yet |
| | Patch coverage threshold is enforced (`codecov.yml`, 80%) and the Codecov check is required | ❌ not required yet |
| | Codacy quality gate reports on PRs and is a required check | ❌ not seen on the latest commit |
| | Workflow files are linted in CI (actionlint, zizmor) | ✅ `pipeline-lint.yml` |
| ☐ | The build is reproducible: runtime versions are pinned (Node 20, Python 3.12) | ✅ |
| ☐ | `concurrency` cancels superseded runs on the same ref | ✅ |
| ☐ | Jobs have a `timeout-minutes` so a hung job can't burn minutes | ✅ |

## 3. Continuous delivery and deployment

| | Item | Status |
|---|---|---|
| ☐ | Build once and deploy that artifact (no rebuild at deploy time) | ✅ frontend |
| ☐ | Production deploys come only from `main` | ✅ frontend |
| ☐ | Deploy is gated on CI success (`needs:`) | ✅ frontend |
| ☐ | A GitHub `environment` is used (approvals, scoped secrets) | ✅ exists; ❓ reviewers not checked |
| ☐ | The backend deploy is automated, not manual `fastapi deploy` | ❌ |
| ☐ | Deploy order is safe: backend and DB changes first, frontend last | ❌ not enforced |
| ☐ | PRs get preview deployments | ❌ |
| ☐ | A post-deploy smoke test hits `/health` and the frontend URL | ❌ |
| ☐ | Netlify's own Git auto-build is off, so there are no duplicate deploys | ✅ confirmed off |

## 4. Security

| | Item | Status |
|---|---|---|
| ☐ | No secrets in the repo or logs; they live in GitHub Secrets or the host's env | ✅ |
| ☐ | Secrets are scoped to the environment that needs them | ❌ repo-level today |
| ☐ | Workflows declare minimal `permissions:` (e.g. `contents: read`) | ✅ |
| ☐ | Third-party actions are pinned to a commit SHA, not a floating tag | ✅ |
| ☐ | CLI tools are version-pinned (`netlify-cli@27.16.3`) | ✅ |
| ☐ | Dependabot or Renovate is enabled (npm, pip, GitHub Actions) | ✅ `dependabot.yml`; ❌ security updates disabled |
| ☐ | Dependency vulnerability scanning runs (`npm audit`, `pip-audit`, Dependabot alerts) | ❌ |
| ☐ | Secret scanning and push protection are enabled in GitHub | ❌ disabled |
| | gitleaks pre-commit hook is configured and installed on each clone | ✅ `.pre-commit-config.yaml`; ❌ not installed in this clone |
| ☐ | Static analysis such as CodeQL runs | ❌ default setup not configured |
| | OpenSSF Scorecard runs weekly | ✅ `scorecard.yml` |
| ☐ | CORS allows only the real frontend origin | ✅ via `CORS_ORIGINS` |
| ☐ | Tokens are rotated on a schedule, and when someone leaves | ❓ |
| ☐ | The Neon DB uses a least-privilege role, not the owner, for the app | ❓ |

## 5. Configuration and environments

| | Item | Status |
|---|---|---|
| ☐ | Config comes from environment variables (12-factor) | ✅ |
| ☐ | `.env.example` files exist and list every variable | ✅ |
| ☐ | Dev, staging and prod are separate (own DB, own URLs) | ❌ one environment only |
| ☐ | Neon branching is used for preview or test databases | ❌ |
| ☐ | Prod and non-prod secrets never share values | ❓ |

## 6. Database and migrations

| | Item | Status |
|---|---|---|
| ☐ | Schema changes use a migration tool (Alembic), not `create_all` | ❌ |
| ☐ | Migrations run in the pipeline before the new code goes live | ❌ |
| ☐ | Migrations are backwards compatible, so old code survives the rollout | ❌ |
| ☐ | Tests run against Postgres, not only SQLite, so CI matches prod | ❌ |
| ☐ | Backups or point-in-time restore are enabled in Neon, and a restore was tried once | ❓ backups unknown; ❌ restore never tried |

## 7. Observability and operations

| | Item | Status |
|---|---|---|
| ☐ | A health endpoint exists and is monitored | ✅ endpoint, ❌ monitor |
| ☐ | Uptime alerts go to a person | ❌ |
| ☐ | Backend logs are structured and reviewable on FastAPI Cloud | ❌ backend not configured on FastAPI Cloud yet |
| ☐ | Error tracking is set up (Sentry or similar) | ❌ |
| ☐ | Failed pipeline runs notify the team | ❓ |
| ☐ | Rollback is documented and tested: Netlify "publish previous deploy", FastAPI Cloud redeploy, Neon restore | ❌ |
| ☐ | Someone owns the pipeline, and a runbook exists for failed deploys | ❌ |

## 8. Documentation

| | Item | Status |
|---|---|---|
| ☐ | README explains local setup, how to run tests, and how deploys work | ❓ backend README still describes the old `backend/static` flow |
| ☐ | Required secrets and variables are documented (names and purpose, not values) | ❌ |
| ☐ | This checklist is reviewed on a schedule, such as quarterly | ❌ |

## Suggested order for this repo

1. Protect `main` and require both CI checks.
2. Add `permissions: contents: read` and `timeout-minutes` to both workflows.
3. Pin actions to SHAs and enable Dependabot, which keeps the pins fresh.
4. Add a deploy job for the backend, then a `/health` smoke test after each deploy.
5. Add lint and frontend tests.
6. Introduce Alembic and run tests against Postgres.

## Required configuration reference

| Name | Kind | Where | Purpose |
|---|---|---|---|
| `NETLIFY_AUTH_TOKEN` | secret | GitHub | Netlify CLI deploy auth |
| `NETLIFY_SITE_ID` | secret | GitHub | Target Netlify site |
| `VITE_API_URL` | variable | GitHub | API base URL baked into the frontend build |
| `CODECOV_TOKEN` | secret | GitHub | Coverage upload from backend CI |
| `DATABASE_URL` | secret | FastAPI Cloud | Neon pooled connection string |
| `CORS_ORIGINS` | variable | FastAPI Cloud | Allowed frontend origin(s) |

## Validating this checklist

Three layers, from most to least automatic.

**1. On every change (enforced in CI)**
- `pipeline-lint.yml` runs actionlint and zizmor on `.github/**`. It fails on unpinned actions, missing
  `permissions:` and injection risks.
- Dependabot opens PRs for npm, pip and GitHub Actions updates, with a 7-day cooldown.
- Developers install the gitleaks pre-commit hook (`pre-commit install`). The audit can check the config file
  but not whether each clone has the hook, so GitHub push protection is the enforced backstop.
- Codecov and Codacy report on each PR. Make both required checks once they are connected.

**2. On demand (`scripts/audit-devops.sh`)**
- Read-only. Needs `gh` (logged in) and `jq`. Prints PASS, FAIL or SKIP per item and exits non-zero on any
  failure.
- Covers branch protection, secrets and variables, the `production` environment, GitHub security features,
  required files, pinned actions, the latest CI runs, and whether Codacy and Codecov reported.
- It lists the checks it can't do (Netlify auto-build, Neon backups, FastAPI Cloud settings, rollback), so
  verify those by hand.

**3. On a schedule**
- OpenSSF Scorecard runs weekly and posts results to the Security tab.
- Review this file quarterly, using the audit output as evidence for each status.
