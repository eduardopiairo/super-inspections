# Schedules

A **Schedule** defines when a [Template](./templates.md) should be run, and for whom — turning
a one-off template into a recurring routine (e.g. "Kitchen Safety, every Monday, Downtown Store").

## Fields

- `template_id` — required; which template to run
- `frequency` — `once`, `daily`, `weekly`, or `monthly`
- `start_date` — when the schedule begins (or the single date it runs, for `once`)
- `site_id` — optional; the site the schedule applies to
- `assigned_user_id` — optional; who is responsible for running it
- `active` — whether the schedule is currently in effect

A schedule is assigned to a **site**, a **user**, or both — e.g. "any assigned user at this
site" vs. "this specific person, wherever they are."

## Relationship to Inspections

A `Schedule` is a plan, not an event log — it doesn't contain answers itself. Each time it fires,
it's expected to produce an [Inspection](./inspections.md) with that schedule's `id` set as
`schedule_id`, so you can trace every inspection back to the schedule that generated it (or see
`schedule_id: null` for inspections created manually, outside any schedule).

> **Not yet implemented:** the actual recurrence engine (a background job that reads `frequency`
> and `start_date` and creates due `Inspection` rows) doesn't exist yet. Today, `Schedule` only
> models *intent* — creating one records the plan, but inspections still have to be created
> manually via the Inspections API.

## API

| Method | Path                | Description                          |
|--------|---------------------|----------------------------------------|
| GET    | `/schedules/`        | List schedules                        |
| POST   | `/schedules/`        | Create a schedule                     |
| GET    | `/schedules/{id}`    | Get a schedule                        |
| DELETE | `/schedules/{id}`    | Delete a schedule                     |

See [backend/app/routers/schedules.py](../backend/app/routers/schedules.py).
