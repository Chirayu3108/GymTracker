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

---

### 2026-07-28 — `users` table field names finalized as built

**Decision:** `password_hash` → `hashed_password`; added `is_active` (boolean, default true) and
`unit_system` (enum: `metric` | `imperial`, default `metric`).

**Why:** Naming matched what was actually written in `app/models/user.py` while implementing
Phase 0 — the doc is updated to track reality rather than drift from it. `is_active` is a
standard soft-disable flag (ban/deactivate a user without deleting their data). `unit_system` is
needed for the canonical-units decision below.

---

### 2026-07-28 — Canonical metric storage for weight/height; unit is a display preference only

**Decision:** Every weight column is stored in kilograms, every height/length column in
centimeters — regardless of what the user entered or wants displayed. `users.unit_system` records
display preference only; conversion to imperial happens at the presentation layer, never in the
database. Applies to `sets.weight`, `routine_exercises.target_weight`, and the new
`body_measurements` table.

**Why:** Prompted by adding `body_measurements` (weight/height tracking) and realizing the
existing schema never actually specified a unit for `sets.weight` / `routine_exercises`. Storing
mixed units per-row (e.g. a `weight_unit` column on every table) would force every consumer of
that data — charts, PR calculations, the "last time" query — to handle unit conversion
defensively. Canonical storage + one display preference is the standard pattern (same approach
apps like Strong/MyFitnessPal use) and keeps aggregation queries simple.

**Revisit if:** a real need emerges for storing exactly what the user typed (e.g. plates on a
barbell in lb vs kg genuinely changing what's loadable) — not expected at this app's scope.

---

### 2026-07-28 — `body_measurements` table added, promoted from vague "stretch" to Phase 2

**Decision:** Added a concrete `body_measurements` table (`weight_kg`, `height_cm`,
`body_fat_percentage`, `muscle_mass_kg`, `recorded_at`), replacing the vague `body_metrics`
placeholder that was previously listed under "stretch, not committed." Slotted into Phase 2
(Progress & Motivation) alongside PRs and progress charts, since it's the same kind of signal —
"am I making progress" — just body composition instead of lift numbers.

**Why:** User requested this table and unit handling be planned now, ahead of Phase 2
implementation, so the schema is settled before Phase 1 work touches `users`.

---

### 2026-07-28 — Branching strategy: one branch per roadmap phase

**Decision:** Work happens on a long-lived branch per phase (e.g. `phase-1-mvp-core-loop`),
merged back to `main` once that phase's feature set actually works end-to-end — not a
branch-per-task/feature model.

**Why:** Solo dev, so there's no concurrent-work conflict risk a finer-grained branch-per-feature
model would normally protect against. The roadmap in
[07-roadmap-phases.md](07-roadmap-phases.md) already chunks work into phase-sized units with a
clear "done" bar (e.g. Phase 1's "dogfood it yourself for real workouts before moving on"), so
branch boundaries matching phase boundaries is close to free — no extra process invented on top
of a plan that already existed.

**Revisit if:** a phase turns out to take long enough that a stale phase-branch starts drifting
meaningfully from `main`, or collaborators ever join and need smaller, independently reviewable
units of work.

---

### 2026-07-29 — Logout is client-side only; no server-side token revocation

**Decision:** `POST /auth/logout` as a backend route is dropped. Logging out means the Flutter
app deletes its locally stored access/refresh tokens — nothing server-side happens.

**Why:** JWTs are stateless by design — the server doesn't track which tokens exist, so
"invalidating" one for real requires extra infrastructure (a revoked/issued-token table checked
on every `/auth/refresh` call). That's real complexity — a table, a cleanup story for expired
entries, a check on the hot path of every refresh — for a capability the MVP doesn't need: no
"log out all devices," no forced revocation on a compromised account. Deleting the local tokens
is sufficient for a single-device, solo-user MVP.

**Revisit if:** multi-device session management, forced logout (e.g. admin action or detected
compromise), or "log out everywhere" ever becomes an actual requirement — at that point a
refresh-token table is the standard fix.

---

### 2026-07-29 — Refresh tokens are non-rotating; JWTs carry a `type` claim

**Decision:** `POST /auth/refresh` returns a new access token but hands back the *same* refresh
token the client sent — it doesn't rotate/reissue one. Separately, every JWT now carries a
`"type"` claim (`"access"` or `"refresh"`), checked explicitly wherever a token is consumed
(`/auth/refresh` requires `"refresh"`, `get_current_user` requires `"access"`).

**Why:** Rotating refresh tokens (issuing a new one on every use, invalidating the old) is the
more defensible pattern against token theft, but it requires exactly the kind of server-side
tracking — a table of currently-valid refresh tokens — that the logout decision above just ruled
out of scope for the MVP. Without that infrastructure, rotation adds complexity without adding
real protection (there's nothing to actually invalidate the *old* token with). The `type` claim,
by contrast, is close to free (one extra field, checked in two places) and closes a real gap:
without it, access and refresh tokens were structurally identical and fully interchangeable at
either endpoint.

**Revisit if:** the no-server-side-tracking constraint changes (see the logout decision above) —
rotation becomes worth adding at the same time a revocation table gets built, not before.
