# Product Overview

## Problem

People who go to the gym consistently want two things most apps make annoyingly hard:

1. **Log a workout fast**, mid-set, without fighting the UI (bad gym wifi, sweaty hands, no
   patience for a 5-tap flow to enter "60kg x 8").
2. **See that they're actually making progress and showing up** — both in terms of numbers
   (progressive overload) and consistency (did I actually go this week?).

Most existing apps are either bloated (nutrition + social + wearables + everything) or too rigid
(fixed exercise programs you can't customize). This app is deliberately narrow: **routines you
define yourself, sessions you log fast, and a clear picture of your consistency and progress.**

## Target user

- Someone already going to the gym (beginner to intermediate lifter), who wants a lightweight
  logbook, not a coach-in-a-box (initially).
- Comfortable on their phone in the gym; wants a web view mainly to review history/plan routines
  on a bigger screen, not necessarily to log sets from a laptop.
- Motivated by visible consistency (streaks, calendar) as much as by raw numbers.

## Core value propositions

1. **Custom routines** — build your own "Push Day", "Leg Day", whatever, from an exercise
   library (+ your own custom exercises).
2. **Fast session logging** — start a session from a routine, log sets/reps/weight per exercise
   with minimal taps, see your last performance on that exercise pre-filled.
3. **Consistency at a glance** — a GitHub-style calendar heatmap of training days, streaks.
4. **Progress over time** — per-exercise history so "what did I lift last time" is always one tap
   away, plus simple charts (weight/volume over time), personal records.
5. **(Later) AI coaching** — recommendations on what weight/reps to attempt next, deload
   suggestions, and eventually natural-language coaching based on your own history.
6. **Everywhere** — iOS, Android, and Web from one codebase, so it's available wherever you are.

## MVP scope (what "done" looks like for v1)

- Account creation / login.
- Exercise library (seeded common exercises + ability to add your own).
- Create/edit/delete custom routines made of exercises with target sets/reps.
- Start a session (from a routine or ad-hoc), log sets with weight/reps, finish the session.
- Session history list + detail view.
- "Last time" values shown while logging (previous weight/reps for that exercise).

Everything else (calendar heatmap, charts, offline support, AI) is explicitly **post-MVP** — see
[07-roadmap-phases.md](07-roadmap-phases.md) for the phased build order. This is intentional: the
core logging loop needs to work and feel good before anything is layered on top of it.

## Explicit non-goals (for now)

Written down so scope creep has to be a conscious decision, not an accident:

- No social features (feeds, following, sharing) — maybe a future stretch phase.
- No nutrition/macro tracking.
- No wearable/device integrations (Apple Health, Garmin, etc.) at launch.
- No pre-built structured programs (e.g. "5/3/1", "PPL 6-day") authored by the app — users build
  their own routines. Could revisit once AI recommendations exist.
- Web is a **companion** experience for planning/reviewing, not the primary logging surface —
  mobile is. Don't over-invest in web-specific UX before mobile is solid.

## Success signals (informal, since this is a personal/early project)

- You (the first user) actually use it in the gym instead of your old method, for at least a few
  weeks straight.
- Logging a set takes a handful of seconds, not a UI hunt.
- Opening the app answers "did I train this week / what's my streak" in under a second.
