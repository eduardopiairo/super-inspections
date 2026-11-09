# CI/CD pipeline

How code gets from a developer's machine to production, and which tool does each stage.
The diagrams are Mermaid, which GitHub renders in the browser.

## General pipeline

Four stages: Version Control, Continuous Integration, Artifact Management, Continuous Delivery.

```mermaid
flowchart LR
    subgraph vc["1. Version Control"]
        direction TB
        git["Git + GitHub<br/>feature/** branch, PR, merge to main"]
    end

    subgraph ci["2. Continuous Integration"]
        direction TB
        cibuild["GitHub Actions<br/>install, test, build"]
    end

    subgraph am["3. Artifact Management"]
        direction TB
        store["GitHub Actions artifacts<br/>frontend-dist (7 days)"]
    end

    subgraph cd["4. Continuous Delivery"]
        direction TB
        fe["Netlify CLI<br/>frontend, automated on main"]
        be["FastAPI Cloud CLI<br/>backend, manual"]
        db[("Neon Postgres")]
        be --> db
    end

    vc -->|push / PR| ci
    ci -->|frontend build| am
    am -->|main only| fe
    ci -.->|source, no artifact| be
```

Solid arrows are automated. Dashed arrows are manual steps (see [devops-checklist.md](./devops-checklist.md)).

## Stages and tools

| Stage | Tools | What happens |
|---|---|---|
| 1. Version Control | Git, GitHub | Work on a `feature/**` branch, open a PR, review, merge to `main` |
| 2. Continuous Integration | GitHub Actions | Backend: Python 3.12, `pip install`, `pytest`. Frontend: Node 20, `npm ci`, `npm test`, `npm run build`. Each runs only when its folder changes |
| 3. Artifact Management | GitHub Actions artifacts | The frontend build (`frontend/dist`) is stored as `frontend-dist` for 7 days. The backend has no artifact, since FastAPI Cloud takes the source |
| 4. Continuous Delivery | Netlify CLI, FastAPI Cloud CLI, Neon | Frontend deploys from `main` through the `production` environment. Backend deploys by hand with `fastapi deploy`. The backend reads `DATABASE_URL` from Neon |

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
