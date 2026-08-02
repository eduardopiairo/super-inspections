# Users & Sites

Minimal reference entities used for assignment across the other concepts — not a full identity
or access-control system.

## Users

- `name`, `email`

Referenced by [Inspections](./inspections.md) (`assigned_user_id`),
[Schedules](./schedules.md) (`assigned_user_id`), and [Actions](./actions.md)
(`assigned_user_id`).

> **Not yet implemented:** there's no authentication, login, or session concept — a `User` row is
> just a name to assign things to, not an account someone can sign in as.

## Sites

- `name`

Represents a physical location (a store, a building, a site) that inspections and actions happen
at. Referenced by [Inspections](./inspections.md), [Schedules](./schedules.md), and
[Actions](./actions.md) (all via `site_id`).

## API

Both follow the same minimal shape:

| Method | Path            | Description       |
|--------|-----------------|--------------------|
| GET    | `/users/`        | List users         |
| POST   | `/users/`        | Create a user       |
| GET    | `/users/{id}`    | Get a user          |
| GET    | `/sites/`        | List sites          |
| POST   | `/sites/`        | Create a site        |
| GET    | `/sites/{id}`    | Get a site           |

See [backend/app/routers/users.py](../backend/app/routers/users.py) and
[backend/app/routers/sites.py](../backend/app/routers/sites.py).
