# Learning Path

Learn just-in-time, tied to what each phase in [07-roadmap-phases.md](07-roadmap-phases.md)
actually needs — not a full curriculum up front. Each topic below lists what to learn and why it
matters for *this specific app*, not generic "learn X" advice.

Official docs are linked because they're the canonical, always-current source for each tool —
prefer them over random tutorials when they conflict.

## 1. Dart basics (Phase 0)

Variables/types, null safety (`?`, `!`, `late`), async/await and `Future`/`Stream`, classes. You
don't need to go deep — enough to read and write Flutter code comfortably.
→ dart.dev/language, dart.dev/codelabs

## 2. Flutter fundamentals (Phase 0–1)

Widget tree mental model (everything is a widget), `StatelessWidget` vs `StatefulWidget`,
layout (`Row`/`Column`/`Expanded`), navigation with `go_router`. Build a couple of throwaway
screens before touching real app code — get the widget-tree intuition first.
→ docs.flutter.dev

## 3. State management with Riverpod (Phase 1)

`Provider`, `FutureProvider`, `AsyncNotifier` — specifically how to model "loading / data / error"
states cleanly, since almost every screen in this app is "fetch from API, show loading, show
data or error." This is the single most-used pattern in the whole app.
→ riverpod.dev

## 4. FastAPI fundamentals (Phase 0–1)

Path/query/body parameters, Pydantic models for request/response, dependency injection
(`Depends`) — used constantly for "get current user from JWT" and "get a DB session." Read the
official tutorial linearly; it's written as a coherent path, not just a reference.
→ fastapi.tiangolo.com

## 5. SQL & PostgreSQL basics, SQLAlchemy + Alembic (Phase 0–1)

Enough SQL to read what SQLAlchemy generates and debug a slow/wrong query: `JOIN`, `GROUP BY`,
`WHERE` with date ranges (used directly for the "last time" lookup and the calendar heatmap
query). Then SQLAlchemy 2.0's ORM patterns (async sessions, relationships), and Alembic for
writing/reviewing migrations rather than hand-editing the schema.
→ docs.sqlalchemy.org, alembic.sqlalchemy.org

## 6. Auth: JWT (Phase 1)

Access token vs. refresh token, why passwords are hashed (bcrypt) not encrypted, where tokens
live on the client (`flutter_secure_storage`) and how to attach/refresh them automatically via a
`dio` interceptor. Understand *why* each piece exists, not just how to copy an auth boilerplate —
this is the part most likely to have a subtle security bug if copied blindly.

## 7. Connecting Flutter to a REST API (Phase 1)

`dio` basics: interceptors (for auth headers and refresh-token retry), error handling, mapping
HTTP errors to user-facing states. Pair this with what you learned in step 3 — the API call
result flows straight into a Riverpod `AsyncNotifier`.

## 8. Data viz + custom widgets (Phase 2)

`fl_chart` basics for line/bar charts (weight/volume over time). Then, as a deliberate "build
something from scratch" exercise: a GitHub-style calendar heatmap using a `GridView` and custom
coloring logic — a good contained project once you're comfortable with basic widgets.

## 9. Offline-first & local storage (Phase 3)

Why naive "just cache the last API response" isn't enough for a true offline-first app; `drift`
for a type-safe local SQLite schema with migrations; the sync pattern described in
[02-architecture.md](02-architecture.md) (queue mutations, push on reconnect, `updated_at`-based
conflict resolution). This is the most conceptually new material in the whole project — budget
real time for it.
→ drift.simonbinder.eu

## 10. Testing (Phase 1 onward, deepens in Phase 3)

`pytest` fixtures and `httpx.AsyncClient` for backend integration tests; `flutter_test` for unit/
widget tests and `integration_test` for end-to-end flows. Start writing tests from Phase 1, not
as a Phase-3 catch-up — see [08-testing-strategy.md](08-testing-strategy.md).

## 11. CI/CD & Docker (Phase 0 basics, Phase 3 depth)

Docker Compose for local dev (Phase 0) is a light introduction. GitHub Actions basics (running
tests on PR) start in Phase 0–1. Deepen in Phase 3: building/signing mobile release artifacts in
CI, deploying the backend container to Railway/Fly.io.

## 12. Deployment specifics (Phase 3)

Containerizing FastAPI for production, environment variable / secrets management, Flutter Web
build + static hosting deploy, and the mobile release process (app signing, TestFlight, Play
Console internal testing track) — each is its own small learning curve the first time.

## 13. LLM API integration (Phase 4)

Calling the Claude API from a backend service: structuring a prompt around a specific narrow
task (workout recommendations) rather than open-ended chat, keeping the API key server-side,
and handling latency/cost/rate limits as a normal external dependency.
→ docs.claude.com

---

**How to actually use this list:** when you start a phase, skim its linked topics *before*
building, then keep the docs open as reference *while* building — don't try to fully learn a
topic in the abstract before touching code. You'll retain far more building the real
"last-time-weight" query than reading about SQL joins in isolation.
