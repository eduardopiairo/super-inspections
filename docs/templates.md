# Templates

A **Template** defines the reusable structure of an inspection — what gets asked, and how the
answer is captured. Teams build a template once (e.g. "Kitchen Safety") and reuse it for every
inspection that follows the same checklist.

## Structure

```
Template
└── Section (ordered)
    └── Question (ordered)
```

- **Template** — `title`, `description`
- **Section** — groups related questions (e.g. "Fire Safety"), has an `order`
- **Question** — the actual prompt, with:
  - `response_type`: `yes_no`, `multiple_choice`, `text`, `photo`, `signature`, `date`
  - `options`: choices, used when `response_type` is `multiple_choice`
  - `required`: whether the question must be answered to complete an inspection
  - `order`: position within its section

A template is created (and updated) with its sections and questions nested in a single request —
there's no separate endpoint for adding one question at a time.

## Why it matters

Everything downstream depends on a template existing first:

- An [Inspection](./inspections.md) is always tied to a template, and its answers are validated
  against that template's questions.
- A [Schedule](./schedules.md) references a template to say what should be run, and how often.

## API

| Method | Path                | Description                                  |
|--------|---------------------|-----------------------------------------------|
| GET    | `/templates/`       | List templates (summary: title + description) |
| POST   | `/templates/`        | Create a template with nested sections/questions |
| GET    | `/templates/{id}`    | Get a template with full sections/questions   |
| PUT    | `/templates/{id}`    | Replace a template's sections/questions       |
| DELETE | `/templates/{id}`    | Delete a template (cascades to sections/questions) |

See [backend/app/routers/templates.py](../backend/app/routers/templates.py).
