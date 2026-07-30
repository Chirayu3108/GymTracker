# API Design

REST over HTTPS, JSON bodies, versioned under `/api/v1`. FastAPI gives automatic interactive docs
(Swagger UI at `/docs`) for free from the route definitions + Pydantic schemas — that becomes the
living API reference; this doc is the design-time plan.

## Conventions

- **Auth**: JWT bearer token in `Authorization: Bearer <token>` header, except `auth/*` routes.
- **Pagination**: cursor or simple `limit`/`offset` query params on list endpoints, response
  shape `{ "items": [...], "total": n }`.
- **Errors**: consistent shape `{ "detail": "human readable message", "code": "machine_code" }`,
  using standard HTTP status codes (400 validation, 401 unauthenticated, 403 forbidden, 404 not
  found, 409 conflict).
- **Timestamps**: ISO 8601, UTC, e.g. `2026-07-25T10:00:00Z`.
- **IDs**: UUIDs everywhere (see [04-database-schema.md](04-database-schema.md)).

## Auth

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/auth/register` | Create account (email + password) |
| POST | `/api/v1/auth/login` | Returns access + refresh token |
| POST | `/api/v1/auth/refresh` | Exchange refresh token for new access token |

Logout has no backend route — see [decisions-log.md](decisions-log.md) (2026-07-29). It's purely
client-side: the app deletes its stored tokens.

## Users

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/users/me` | Current user profile |
| PATCH | `/api/v1/users/me` | Update display name etc. |

## Exercises

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/exercises?muscle_group=&search=` | Browse/search library (seeded + user's own custom) |
| POST | `/api/v1/exercises` | Create a custom exercise |
| GET | `/api/v1/exercises/{id}` | Detail |
| PATCH | `/api/v1/exercises/{id}` | Edit (only own custom exercises) |
| DELETE | `/api/v1/exercises/{id}` | Delete (only own custom exercises) |

## Routines

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/routines` | List current user's routines |
| POST | `/api/v1/routines` | Create routine (name, description) |
| GET | `/api/v1/routines/{id}` | Detail, including its exercises |
| PATCH | `/api/v1/routines/{id}` | Edit / archive |
| DELETE | `/api/v1/routines/{id}` | Delete |
| POST | `/api/v1/routines/{id}/exercises` | Add an exercise to the routine (order, targets) |
| PATCH | `/api/v1/routines/{id}/exercises/{routine_exercise_id}` | Edit order/targets |
| DELETE | `/api/v1/routines/{id}/exercises/{routine_exercise_id}` | Remove from routine |

## Sessions

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/sessions?from=&to=&limit=&offset=` | History, paginated, optional date range |
| POST | `/api/v1/sessions` | Start a session (optional `routine_id`; copies routine's exercises in as a starting point) |
| GET | `/api/v1/sessions/{id}` | Full detail: exercises + sets |
| PATCH | `/api/v1/sessions/{id}` | Edit notes etc. |
| POST | `/api/v1/sessions/{id}/complete` | Mark finished (`ended_at`) |
| DELETE | `/api/v1/sessions/{id}` | Delete a session |
| POST | `/api/v1/sessions/{id}/exercises` | Add an exercise to an in-progress session |
| DELETE | `/api/v1/sessions/{id}/exercises/{session_exercise_id}` | Remove |
| POST | `/api/v1/sessions/{id}/exercises/{session_exercise_id}/sets` | Log a set (weight, reps, is_warmup) |
| PATCH | `/api/v1/sessions/{id}/exercises/{session_exercise_id}/sets/{set_id}` | Edit a logged set |
| DELETE | `/api/v1/sessions/{id}/exercises/{session_exercise_id}/sets/{set_id}` | Delete a logged set |

## Stats (Phase 2+)

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/stats/calendar?year=2026` | `{ "2026-07-25": 1, ... }` map of date → trained (or session count) for the heatmap |
| GET | `/api/v1/stats/streak` | Current streak + longest streak |
| GET | `/api/v1/stats/exercises/{exercise_id}/history` | Time series of weight/reps/volume for charts |
| GET | `/api/v1/stats/exercises/{exercise_id}/last` | Quick "what did I lift last time" lookup |
| GET | `/api/v1/stats/exercises/{exercise_id}/records` | Personal records for that exercise |

## Sync (Phase 3, offline-first)

Not part of the MVP API surface. When Phase 3 lands, a batch endpoint is added rather than
retrofitting sync onto every individual endpoint:

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/sync` | Body: pending local mutations since last sync + `last_synced_at`. Response: server-side changes since that timestamp, plus conflict resolutions. |

Until then, the client talks to the endpoints above directly, one call per action, over plain
HTTPS — simplest possible approach for the MVP.

## AI recommendations (Phase 4)

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/exercises/{exercise_id}/recommendation` | Rule-based (4a) or LLM-based (4b) suggestion for next attempt, given history |

Kept as its own endpoint rather than baked into the session-logging flow, so it can be called
lazily (e.g. only when the user taps "suggest") without adding latency to the core logging path.
