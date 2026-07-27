# Tech Stack

Every choice below has a "why this, not that" — this is a solo learning project, so tools that
are well-documented and widely used beat tools that are theoretically better but leave you
stuck alone with an obscure error at 11pm.

## Frontend — Flutter

| Concern | Choice | Why |
|---|---|---|
| Framework | **Flutter (Dart)** | Single codebase compiles natively to iOS, Android, and Web. Chosen over React Native (great too, but Flutter's story for all 3 targets — especially Web — is more unified) and Kotlin Multiplatform (would mean maintaining 3 separate UI layers: Compose + SwiftUI + a web app, too much for solo dev). |
| State management | **Riverpod** | Less boilerplate than Bloc, more testable/scalable than plain `Provider` or `setState`. Compile-safe, works well with async data (API calls) via `FutureProvider`/`AsyncNotifier`. |
| Navigation | **go_router** | The de-facto standard for declarative routing in Flutter, has good deep-linking support (matters for Web). |
| Local storage (Phase 3+) | **drift** | Type-safe SQLite wrapper with schema migrations built in — needed for the offline-first work in Phase 3. |
| Secure token storage | **flutter_secure_storage** | Keeps JWT tokens out of plain SharedPreferences. |
| Networking | **dio** | More ergonomic than raw `http` for interceptors (auth headers, refresh-token retry logic), which this app needs. |
| Charts | **fl_chart** | Most mature charting package in the Flutter /plan i want you to plan this project for me from starting you can write everything in docs. I want to use docs folder to write different thing. This is a gym app which will help the user to keep track of their progress and create their own exercise sessions like Push day or chest day something like that. and they can start the session. Then i will also have a calender view kind of thing like github which will show how many days you did go to the gym. This basically is an app for people to keep their progress. This app will have the easiest UI for people and better UX. I might also add AI later on which will help and give recommendation to the users. It will keep track like what weight they did last time. I want the app for IOS Android and Web. I want you to be careful and write what all the docs would i need and what are app architecture design should i use and what tech stack. then what should be database structure like. I will code the app by my own but i want you to give me the plan i will learn new tech as i go but you will have to teach me that as well. Also we need to be careful as we also might have to create many testsecosystem for the progress-over-time graphs. |
| Calendar heatmap | Custom widget (Phase 2) | No off-the-shelf package matches a GitHub-style heatmap well enough — build a small custom `GridView`-based widget. Treat this as a good, contained first "build something visual from scratch" exercise. |
| Design system | **Material 3** (Flutter default) | Ships with Flutter, has a light/dark theme story out of the box, is the least-effort path to a clean, consistent UI. |

**Note on Flutter Web**: it's a real, supported target, but historically has trade-offs (larger
initial bundle size, less "native web" feel, weaker SEO — irrelevant for a logged-in app). Treat
it as a genuinely secondary surface per [01-product-overview.md](01-product-overview.md) — get
mobile right first, then verify Web as you go rather than pixel-perfecting it early.

## Backend — Python / FastAPI

| Concern | Choice | Why |
|---|---|---|
| Language/runtime | **Python 3.12+** | Matches the existing `backend/main.py` starting point. |
| Framework | **FastAPI** | Async-native, automatic OpenAPI docs (huge for a solo dev testing your own API), and Pydantic-based validation means request/response shapes are enforced, not just hoped for. |
| ORM | **SQLAlchemy 2.0 (async)** | The standard, mature Python ORM; async mode pairs naturally with FastAPI's async request handling. |
| Migrations | **Alembic** | SQLAlchemy's companion migration tool — versioned, reviewable schema changes instead of hand-editing the DB. |
| Validation/schemas | **Pydantic v2** | Ships with FastAPI; used for request/response schemas, kept separate from SQLAlchemy models (see [02-architecture.md](02-architecture.md)). |
| Auth | **JWT** (access + refresh tokens) via `python-jose` or `PyJWT`, passwords hashed with `passlib`/`bcrypt` | Standard, stateless auth that works cleanly for a mobile+web client without server-side session storage. |
| Database | **PostgreSQL** | Relational data (users → routines → exercises → sessions → sets) is a textbook relational model; Postgres is free, robust, and has excellent managed hosting options. |
| Local dev | **Docker Compose** (API container + Postgres container) | One command to get a working local backend, no "works on my machine" DB setup drift. |

## AI (Phase 4, later)

- **Phase 4a**: no ML at all — simple rule-based logic in the service layer (e.g. "you did 3x8 @
  60kg last time and hit all reps → suggest 62.5kg next time"). This alone covers most of what
  people actually want from "AI" recommendations, at zero cost and zero new infrastructure.
- **Phase 4b**: natural-language coaching via the **Claude API** (Anthropic), called from the
  FastAPI backend (never directly from the client, to keep the API key server-side and control
  cost/rate limits), using the user's own workout history as context.

## DevOps / tooling

| Concern | Choice | Why |
|---|---|---|
| Source control | **GitHub** (already set up) | — |
| CI | **GitHub Actions** | Run backend tests (pytest) + frontend tests (`flutter test`, `flutter analyze`) on every PR. |
| Backend hosting | **Railway or Fly.io** | Cheap, simple single-container deploys, good free/low tiers for a solo project. |
| Managed Postgres | **Neon** or **Supabase Postgres** (or the host's own Postgres add-on) | Serverless/managed, generous free tier, no ops burden. |
| Web hosting | **Firebase Hosting** or **Cloudflare Pages** | Static hosting for the Flutter Web build. |
| Error monitoring (post-MVP) | **Sentry** | Has both Flutter and Python SDKs — add once there are real users to monitor for. |

## Explicitly deferred / not chosen

- **GraphQL** — REST is simpler to reason about, debug, and document (via FastAPI's automatic
  OpenAPI/Swagger UI) for an API this size. Revisit only if the client ends up needing deeply
  nested, flexible queries that REST makes awkward — unlikely here.
- **Microservices / message queues** — no scale problem exists yet to justify the operational
  complexity. See "Scale posture" in [02-architecture.md](02-architecture.md).
- **Native per-platform apps (Swift/Kotlin)** — would give the most "native" feel but at 3x the
  UI maintenance burden for a solo dev; explicitly ruled out in favor of Flutter.
