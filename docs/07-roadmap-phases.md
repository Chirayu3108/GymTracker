# Roadmap — Phased Build Order

Each phase has a feature scope and a "what you'll learn" callout — the two are deliberately
built together, so the plan doubles as the curriculum in [09-learning-path.md](09-learning-path.md).
Don't start a phase's features before at least skimming its linked learning topics.

## Phase 0 — Setup & Foundations

**Goal:** a Flutter app and a FastAPI backend that can talk to each other, deployed nowhere yet,
just running locally.

- Scaffold the Flutter project with iOS, Android, and Web targets enabled.
- Scaffold the FastAPI project in `backend/` (already has an empty `main.py` — start here),
  with Docker Compose running API + Postgres locally.
- Set up Alembic, create the `users` table migration.
- One real endpoint: `GET /health`. One real screen: the Flutter app calls it and shows the
  result.
- Basic GitHub Actions CI skeleton (even if it just runs `flutter analyze` + a placeholder
  pytest run).

**Learn:** Dart basics, Flutter widget basics, FastAPI basics, Docker Compose basics, git/GitHub
workflow if rusty.

## Phase 1 — MVP: Core Logging Loop

**Goal:** you can actually use this app for a real workout, end to end.

- Auth: register, login, JWT storage on device, logout.
- Exercise library: seed ~50–100 common exercises; browse/search.
- Routines: create/edit/delete a routine, add exercises with target sets/reps.
- Sessions: start a session (from a routine or ad-hoc), log sets (weight + reps) per exercise,
  finish the session.
- Session history: simple list + detail view of past sessions.
- "Last time" values shown when logging a set for an exercise.

**Learn:** Riverpod state management, Flutter forms/navigation (go_router), SQLAlchemy models +
Alembic migrations, JWT auth end to end, connecting Flutter to a REST API with `dio`.

**This is the phase that matters most** — everything after this is enhancement. Dogfood it
yourself for real workouts before moving on.

## Phase 2 — Progress & Motivation

**Goal:** the app answers "am I actually making progress / showing up" at a glance.

- GitHub-style calendar heatmap of training days (custom Flutter widget).
- Streak calculation (current + longest), surfaced on the home screen.
- Per-exercise progress charts (weight/volume over time) via `fl_chart`.
- Personal records tracking (max weight, estimated 1RM, max volume) with a cached
  `personal_records` table.

**Learn:** aggregation queries in SQL/SQLAlchemy, building a custom grid-based widget in Flutter,
`fl_chart` basics, thinking about what to cache vs. compute on read.

## Phase 3 — Offline-First & Polish

**Goal:** the app is reliable in a gym with bad signal, and feels genuinely polished.

- Local SQLite via `drift` as the client's source of truth during a session.
- Sync engine: queue mutations offline, push on reconnect, `POST /api/v1/sync` batch endpoint,
  last-write-wins conflict resolution via `updated_at`.
- UX polish pass: animations, empty states, onboarding flow, dark mode verification.
- Push notification reminders (optional — evaluate if it's actually wanted before building).
- Testing hardening (see [08-testing-strategy.md](08-testing-strategy.md)) and CI/CD pipeline to
  TestFlight (iOS) and Play Console internal testing (Android).

**Learn:** offline-first sync patterns, `drift` schema/migrations, mobile release process
(signing, TestFlight, Play Console), `flutter_test`/`integration_test`, GitHub Actions for
mobile builds.

## Phase 4 — AI Recommendations

**Goal:** the app starts giving genuinely useful suggestions, not just logging what already
happened.

- **4a — rule-based:** simple heuristics in the backend service layer (progressive overload
  suggestions, deload detection when performance drops) — no ML, no external API, ships fast.
- **4b — LLM-based:** natural-language coaching via the Claude API, called server-side with the
  user's workout history as context, exposed through `GET /exercises/{id}/recommendation`.

**Learn:** prompt design for a specific, narrow use case; calling an LLM API securely from a
backend; handling latency/cost/rate limits for a third-party API dependency.

## Phase 5 — Stretch / Future (not committed)

Explicitly speculative — don't plan concretely for these until Phases 0–4 are done and you know
what's actually missing:

- Social features (share routines, follow friends).
- Wearable integrations (Apple Health, etc.).
- Nutrition tracking.
- A more fully-featured Web experience, if usage data shows people actually want to log from
  Web rather than just review there.
