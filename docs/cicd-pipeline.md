# CI/CD pipeline

How code gets from a developer's machine to production, and which tool does each stage.
The diagrams are Mermaid, which GitHub renders in the browser.

Solid arrows are automated. Dashed arrows are manual steps that are not automated yet (see
[devops-checklist.md](./devops-checklist.md)).

## End-to-end flow

```mermaid
flowchart LR
    dev["Developer<br/>VS Code + Git"] -->|push feature/**| gh[("GitHub<br/>repo")]
    gh -->|open PR| pr{{"Pull request"}}

    subgraph ci["Continuous integration - GitHub Actions"]
        direction TB
        be["backend-ci.yml<br/>(on backend/** changes)<br/>Python 3.12, pip, pytest"]
        fe["frontend-ci.yml: build-and-test<br/>(on frontend/** changes)<br/>Node 20, npm ci, npm test, vite build"]
    end

    gh --> ci
    pr --> ci
    ci -->|checks pass| merge["Review + merge to main"]
    merge --> gh

    subgraph cdfe["Frontend CD - GitHub Actions, main only"]
        direction TB
        art["Artifact: frontend-dist<br/>(upload-artifact)"]
        dep["deploy job<br/>environment: production<br/>netlify-cli deploy --prod"]
        art --> dep
    end

    fe -.->|on main| art
    dep --> netlify["Netlify CDN<br/>static frontend"]

    merge -. "manual: fastapi deploy" .-> fcloud["FastAPI Cloud<br/>FastAPI backend"]
    fcloud --> neon[("Neon<br/>Postgres")]

    netlify -->|"HTTPS, VITE_API_URL"| fcloud
```

## Stages and tools

| Stage | Trigger | Tool | What happens |
|---|---|---|---|
| Code | local | Git, VS Code | Work on a `feature/**` branch |
| Source | push, PR | GitHub | Hosts the repo and runs the checks |
| Backend CI | `backend/**` change on push or PR | GitHub Actions | Set up Python 3.12, `pip install -e ".[test]"`, `pytest` |
| Frontend CI | `frontend/**` change on push or PR | GitHub Actions | Set up Node 20, `npm ci`, `npm test --if-present`, `npm run build` |
| Package | after frontend build | GitHub Actions artifacts | `frontend/dist` is stored as `frontend-dist` for 7 days |
| Frontend CD | push to `main`, CI green | GitHub Actions + Netlify CLI | The `production` environment job downloads the artifact and deploys it |
| Frontend host | after deploy | Netlify | Serves the static files from its CDN |
| Backend CD | manual | FastAPI Cloud CLI | `fastapi deploy` from `backend/` |
| Backend host | after deploy | FastAPI Cloud | Runs the API, with `DATABASE_URL` and `CORS_ORIGINS` set in its settings |
| Database | runtime | Neon | Serverless Postgres, reached through the pooled connection string |

## Frontend workflow in detail

```mermaid
flowchart TB
    t["Trigger<br/>push to main / feature/**, or PR<br/>paths: frontend/**"] --> c["concurrency:<br/>cancel superseded runs"]
    c --> j1

    subgraph j1["Job: build-and-test"]
        direction TB
        s1["checkout"] --> s2["setup-node 20 + npm cache"]
        s2 --> s3["npm ci"]
        s3 --> s4["npm test --if-present"]
        s4 --> s5["npm run build<br/>VITE_API_URL from repo variable"]
        s5 --> s6["upload-artifact frontend-dist"]
    end

    j1 --> g{"push to main?"}
    g -- no --> stop(["stop: PRs and feature branches never deploy"])
    g -- yes --> j2

    subgraph j2["Job: deploy - environment: production"]
        direction TB
        d1["checkout"] --> d2["download-artifact frontend-dist"]
        d2 --> d3["netlify deploy --prod --no-build<br/>NETLIFY_AUTH_TOKEN, NETLIFY_SITE_ID"]
    end

    j2 --> live(["Live on Netlify"])
```

## Backend workflow in detail

```mermaid
flowchart TB
    t["Trigger<br/>push to main / feature/**, or PR<br/>paths: backend/**"] --> j

    subgraph j["Job: build-and-test"]
        direction TB
        s1["checkout"] --> s2["setup-python 3.12 + pip cache"]
        s2 --> s3["pip install -e '.[test]'"]
        s3 --> s4["pytest -v<br/>SQLite test DB"]
    end

    j --> done(["Checks reported on the PR"])
    done -.->|manual| m["fastapi deploy"]
    m --> live(["Live on FastAPI Cloud, using Neon Postgres"])
```

## Gaps this diagram shows

- The backend has no automated deploy, so the dashed arrow is a person running a command.
- Nothing orders the two deploys. If an API change and a frontend change merge together, the frontend can
  go live before the backend is ready.
- There is no step after deploy that checks the site is up.
- There is no migration step. The app creates tables on startup.
