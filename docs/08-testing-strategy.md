# Testing Strategy

The user explicitly wants tests taken seriously. Below is the pyramid for both stacks, kept
proportionate to a solo-dev project — thorough where correctness actually matters (money-equivalent:
your own workout history), lighter where it doesn't (pure UI styling).

## Backend (FastAPI) — pytest

| Layer | Tool | What it covers |
|---|---|---|
| Unit | `pytest` | Service-layer functions in isolation: streak calculation, PR calculation, "last time" lookup logic. These are pure-ish functions given a DB session — the highest-value tests in the app, since a bug here silently corrupts what the user sees about their own progress. |
| Integration | `pytest` + `httpx.AsyncClient` | Full request → router → service → DB → response, against a real test Postgres (not SQLite — Postgres-specific behavior, e.g. enums/constraints, should be tested against Postgres itself). |
| Fixtures | `pytest` fixtures | Test user + auth headers, seeded exercises, a reusable "build a routine/session" factory fixture. |

**Test DB isolation:** each test runs in a transaction that's rolled back at the end (or a fresh
schema per test session if that gets complicated) — never share mutable state between tests.

**Coverage target:** aim for 70–80% on `services/` and `api/`, not 100% everywhere. Don't write
tests for framework glue (e.g. that Pydantic validates a required field — that's FastAPI's job to
have already tested).

## Frontend (Flutter)

| Layer | Tool | What it covers |
|---|---|---|
| Unit | `flutter_test` | Riverpod providers/notifiers in isolation (e.g. does the session-logging state machine transition correctly), pure logic (date range math for the calendar). |
| Widget | `flutter_test` | Individual screens/components render correctly given mocked providers — e.g. "the active session screen shows the last-time weight as a hint." |
| Golden | `flutter_test` golden tests | Snapshot tests for key screens to catch visual regressions — worth it specifically because "easiest UI, better UX" is a stated product goal, so unintended visual drift should fail CI, not get noticed by eye later. |
| Integration | `integration_test` package | Full user flows on a real simulator/emulator: login → create routine → start session → log sets → finish → see it in history. Run these for the handful of flows that actually matter, not every possible path. |

## CI (GitHub Actions)

On every PR:
- Backend: `pytest` (with a Postgres service container), plus lint (`ruff`) and type checks if
  using them.
- Frontend: `flutter analyze`, `dart format --set-exit-if-changed`, `flutter test`.
- Merge is blocked on any of the above failing.

Integration tests (the slower simulator-based ones) run less frequently — e.g. nightly or
pre-release — rather than on every PR, to keep the PR feedback loop fast.

## Manual/exploratory testing

Automated tests catch regressions; they don't catch "this flow feels clunky." Before each
release (especially anything touching the active-session logging screen — the most-used screen
in the app), do a real pass on a physical device with a short UX checklist:

- Can you log a full workout using only the app, one-handed, without confusion?
- Does every primary action complete in a small, predictable number of taps?
- No janky animations, no layout shifts, tap targets feel comfortable.
- Dark mode looks correct, not just "doesn't crash."

This is deliberately not automatable — it's a judgment pass on product feel, done by you as the
first real user, tied back to the UX principles in [10-ui-ux-guidelines.md](10-ui-ux-guidelines.md).
