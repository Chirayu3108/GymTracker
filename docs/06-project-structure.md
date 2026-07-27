# Project Structure

Single repo, two apps, shared docs. Matches the existing `backend/` and `frontend/` folders
already in this repo.

```
GymTracker/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI app entrypoint
│   │   ├── core/                  # config, security (JWT, password hashing)
│   │   ├── api/
│   │   │   └── v1/                # routers: auth.py, users.py, exercises.py,
│   │   │                          #   routines.py, sessions.py, stats.py
│   │   ├── models/                # SQLAlchemy ORM models
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   ├── services/               # business logic (one module per domain area)
│   │   └── db/                     # session setup, base class
│   ├── alembic/                    # migrations
│   ├── tests/                      # pytest (mirrors app/ structure)
│   ├── Dockerfile
│   ├── docker-compose.yml          # API + Postgres for local dev
│   └── pyproject.toml              # deps + tool config (ruff, pytest, etc.)
│
├── frontend/
│   ├── lib/
│   │   ├── main.dart
│   │   ├── app/                    # routing (go_router), theme, app-wide setup
│   │   ├── core/                   # networking (dio client), local db (drift, Phase 3+),
│   │   │                          #   shared models, auth token storage
│   │   ├── features/               # one folder per feature, feature-first structure
│   │   │   ├── auth/
│   │   │   ├── exercises/
│   │   │   ├── routines/
│   │   │   ├── sessions/           # the active-session logging screen lives here
│   │   │   ├── calendar/
│   │   │   └── stats/
│   │   └── widgets/                 # shared/reusable UI components
│   ├── test/                        # unit + widget tests, mirrors lib/ structure
│   ├── integration_test/            # end-to-end flows
│   └── pubspec.yaml
│
├── docs/                            # this folder
└── .github/
    └── workflows/                   # CI: backend tests, frontend tests, lint
```

## Why feature-first for Flutter

Each folder under `features/` (e.g. `sessions/`) owns its own screens, widgets, and Riverpod
providers for that feature. This scales better than organizing top-level by *type*
(`screens/`, `widgets/`, `providers/` each containing files from every feature mixed together) —
when you're working on the active-session logging flow, everything relevant lives in one folder,
which matters a lot when you're learning the framework and don't want to be hunting across five
top-level directories for related code.

`core/` and `widgets/` hold only what's genuinely shared across 2+ features (the API client,
auth token handling, buttons/inputs used everywhere) — resist the urge to put feature-specific
code there "just in case."

## Why layered for FastAPI

The reverse logic applies on the backend: `routers/`, `services/`, `models/`, `schemas/` are
organized by *layer*, not by feature, because the backend is small enough that navigating by
layer (see [02-architecture.md](02-architecture.md) for what each layer does) is more useful than
navigating by domain — and it keeps HTTP concerns, business logic, and data access from bleeding
into each other, which is the actual goal of layering.

## Tests mirror source structure

Both `backend/tests/` and `frontend/test/` mirror their respective `app/`/`lib/` trees file for
file, so it's always obvious where a given piece of code's tests live. Details in
[08-testing-strategy.md](08-testing-strategy.md).
