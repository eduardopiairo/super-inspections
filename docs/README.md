# Concepts

Super Inspections is built around five core concepts. This is the reading order — each one
builds on the last:

1. [Templates](./templates.md) — the reusable structure of an inspection (sections and questions)
2. [Inspections](./inspections.md) — a single run of a template, with answers
3. [Schedules](./schedules.md) — recurring or one-off plans that generate inspections
4. [Actions](./actions.md) — trackable follow-up tasks, from an inspection or standalone
5. [Users & Sites](./users-and-sites.md) — who things are assigned to, and where

## How they relate

```
Template ──< Section ──< Question
   │                         │
   │                         │
   ├──< Schedule             │
   │       │                 │
   │       └──> Inspection ──┤
   │               │         │
   └──────────────>│         │
                    ├──< Answer (per Question)
                    └──< Action (optionally per Question)

Action ──> Site / User (standalone, no Inspection required)
```

A `Template` defines the questions once. A `Schedule` says *when* and *for whom* those questions
get asked again. An `Inspection` is one occurrence of answering them. An `Action` is what happens
when something needs fixing — either raised from a specific answer, or created on its own.
