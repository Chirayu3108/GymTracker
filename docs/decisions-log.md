# Decisions Log

A running record of real decisions and why they were made — not a full ADR process, just enough
to answer "why did we do it this way" months from now without having to reconstruct the reasoning.
Append to this file as new decisions get made; don't edit past entries except to correct facts —
add a new entry if a decision is reversed.

---

### 2026-07-25 — Flutter for the client (iOS, Android, Web)

**Decision:** Build the client in Flutter/Dart, single codebase for all three platforms.

**Why:** Needed one codebase to realistically cover iOS + Android + Web as a solo dev. Considered
against React Native + Expo (excellent ecosystem and learning resources, but web is more of an
afterthought there) and Kotlin Multiplatform (best native feel, but means maintaining three
separate UI layers — Compose, SwiftUI, and a web app — which is too much surface area for one
person). Flutter's story for genuinely sharing UI across all three targets, including Web, was
the deciding factor.

**Revisit if:** Flutter Web's limitations (bundle size, non-"native web" feel) become a real
problem once Web usage data exists — see [01-product-overview.md](01-product-overview.md), Web
was always scoped as a secondary surface.

---

### 2026-07-25 — FastAPI + PostgreSQL for the backend

**Decision:** Python 3.12+, FastAPI, SQLAlchemy 2.0 (async) + Alembic, PostgreSQL.

**Why:** The repo already had an empty `backend/main.py`, signaling a Python-first intent.
FastAPI is well-suited to a solo/learning context: automatic OpenAPI docs act as a live API
reference without extra effort, and Pydantic-based validation catches contract mismatches early.
PostgreSQL was an easy call — the data (users → routines → exercises → sessions → sets) is
textbook relational, and Postgres has excellent free/cheap managed hosting.

---

### 2026-07-25 — REST, not GraphQL

**Decision:** Plain REST API under `/api/v1`.

**Why:** Simpler to build, debug, and document solo. FastAPI's automatic Swagger UI gives most
of the "explorable API" benefit people reach for GraphQL for, without the added client/server
complexity. Revisit only if the client ends up needing deeply nested, flexible queries that REST
makes genuinely awkward — not expected at this app's scope.

---

### 2026-07-25 — Offline-first is real, but deferred to Phase 3

**Decision:** MVP (Phase 1) ships online-only. Local-first storage (`drift`) and a sync engine
are built in Phase 3, not the MVP.

**Why:** Gym connectivity is genuinely bad often enough that offline support matters long-term —
this isn't being dismissed. But building a full sync engine before the data model has been
proven against real usage risks designing the wrong thing. The compromise: **UUID primary keys
and `updated_at`/soft-delete columns are required from the MVP schema onward** (see
[04-database-schema.md](04-database-schema.md)) specifically so Phase 3 doesn't require a
breaking schema migration — only the sync logic itself is deferred, not the schema decisions that
enable it.

---

### 2026-07-25 — Rule-based recommendations before any ML/LLM

**Decision:** Phase 4 splits into 4a (simple heuristics, e.g. progressive-overload suggestions
computed in the backend service layer) before 4b (Claude API-based natural language coaching).

**Why:** Most of the practical value of "AI recommendations" for this use case (suggest a next
weight, flag a deload) doesn't need a model at all — it needs the user's own history and a
handful of rules. Shipping that first delivers real value with zero new infrastructure or cost,
and validates what recommendations are actually useful before investing in LLM integration.
