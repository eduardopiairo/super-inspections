# Actions

**Actions** let a team identify, track, and complete follow-up tasks. An action can be raised
from a specific answer while conducting an inspection, or created standalone — "on the go,"
without starting an inspection at all.

## Fields

- `description` — required; what needs to be done
- `status` — `open`, `in_progress`, or `done`
- `assigned_user_id` — optional; who is responsible
- `due_date` — optional
- `frequency` — `once`, `daily`, `weekly`, or `monthly`; for recurring tasks like routine
  maintenance checks, so they're never missed

## Two ways an Action gets created

**From an inspection** — raised against a specific answer:
- `inspection_id` — the inspection it was raised from
- `question_id` — the specific question/answer that triggered it (e.g. a failed "Extinguisher
  present?" check)

**Standalone** — no inspection involved:
- `inspection_id` is `null`
- `site_id` — optional; gives a standalone action a location, since there's no inspection to
  imply one (e.g. "Fix broken tile" at a specific site, spotted while walking around)

A `question_id` only makes sense in the context of an inspection, so setting it without an
`inspection_id` is rejected.

> **Not yet implemented:** like Schedules, `frequency` on an Action currently just records intent
> — there's no background job yet that automatically spawns a new Action instance each time it
> recurs.

## API

| Method | Path              | Description                                  |
|--------|-------------------|------------------------------------------------|
| GET    | `/actions/`        | List actions                                  |
| POST   | `/actions/`         | Create an action (inspection-linked or standalone) |
| GET    | `/actions/{id}`    | Get an action                                  |
| PATCH  | `/actions/{id}`    | Update status, assignee, due date, frequency   |
| DELETE | `/actions/{id}`    | Delete an action                               |

See [backend/app/routers/actions.py](../backend/app/routers/actions.py).
