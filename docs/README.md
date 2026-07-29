# Gym Tracker — Planning Docs

This folder is the single source of truth for planning this project before (and while) it's built.
Nothing in here is code — it's the map. Update these docs as decisions change; they're meant to
stay alive, not be a one-time dump.

## How to use this folder

Read in this order the first time. After that, treat each file as a reference you dip into.

| # | Doc | What it answers |
|---|-----|------------------|
| 1 | [01-product-overview.md](01-product-overview.md) | What are we building and for whom? What's in/out of scope? |
| 2 | [02-architecture.md](02-architecture.md) | How do the pieces fit together? Client-server, offline strategy. |
| 3 | [03-tech-stack.md](03-tech-stack.md) | What exact tools/libraries, and why these over alternatives. |
| 4 | [04-database-schema.md](04-database-schema.md) | What tables, columns, relationships. |
| 5 | [05-api-design.md](05-api-design.md) | What endpoints the backend exposes and how the client calls them. |
| 6 | [06-project-structure.md](06-project-structure.md) | How folders/files are organized in both apps. |
| 7 | [07-roadmap-phases.md](07-roadmap-phases.md) | What gets built in what order, phase by phase. |
| 8 | [08-testing-strategy.md](08-testing-strategy.md) | How we know it works, at each layer. |
| 9 | [09-learning-path.md](09-learning-path.md) | What to learn, in what order, to execute this plan. |
| 10 | [10-ui-ux-guidelines.md](10-ui-ux-guidelines.md) | Design principles and the key screens. |
| 11 | [decisions-log.md](decisions-log.md) | Why we chose what we chose (running log, add to it over time). |
| 12 | [learning-log.md](learning-log.md) | Session-by-session record of what got built and what was learned (with gotchas), including the messy debugging detail decisions-log.md deliberately leaves out. |

## Project one-liner

A cross-platform (iOS, Android, Web) gym tracking app where users build their own workout
routines (e.g. "Push Day"), run sessions against them, and see their consistency and progress
over time via a GitHub-style calendar heatmap — with AI-driven coaching recommendations planned
as a later phase.

## Ground rules for this plan

- **Solo dev, learning as you go.** Every phase in the roadmap is scoped to be learnable, not just
  buildable. [09-learning-path.md](09-learning-path.md) exists specifically to teach the tech
  each phase needs, in order.
- **Ship the core loop first.** Auth → routines → sessions → history, all online-only, before
  anything fancier (offline sync, AI, calendar heatmap polish).
- **Simplicity over cleverness.** Fewest moving parts that get the job done. Every "add X later"
  note in these docs is deliberate — not a placeholder for scope creep now.
- **These docs will get stale.** When a real decision diverges from what's written here, update
  the doc in the same sitting. A wrong doc is worse than no doc.
