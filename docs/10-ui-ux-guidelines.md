# UI/UX Guidelines

The product goal is explicitly "easiest UI, better UX" — this doc turns that into concrete rules,
not just a vibe.

## Principles

1. **Minimize taps to log a set.** This is the single most-repeated action in the app (dozens of
   times per workout) — it should be a number pad or steppers pre-filled with the last-time
   value, one or two taps to confirm, done. Every extra tap here is multiplied by every set of
   every workout, forever.
2. **One primary action per screen.** The home screen's obvious, dominant action is "Start
   Session." Don't compete with it — secondary actions (view history, edit routines) are visibly
   secondary.
3. **Bottom navigation, max ~5 tabs.** Suggested: Home (today + streak + quick start), Routines,
   History/Calendar, Stats, Profile. If a 6th tab feels needed later, that's a sign to consolidate,
   not to add a 6th tab.
4. **Dark mode from day one.** Gym environments and night use make this a real requirement, not
   a nice-to-have polish item — build both themes together, not light-first-then-retrofit.
5. **Rest timer is glanceable.** Large, high-contrast, visible from arm's length between sets.
6. **Empty states always have a clear next action.** A new user's routine list isn't just blank —
   it says "Create your first routine" with a button right there.
7. **Accessibility basics, not an afterthought.** Minimum ~44×44pt tap targets, sufficient color
   contrast (matters doubly for a heatmap, which is inherently color-coded), text that respects
   system font-scaling settings.

## Calendar heatmap (the GitHub-style view)

- Grid of day-cells, color intensity mapped to something meaningful — simplest version: binary
  (trained / didn't), better version: intensity by session count or volume that day.
- Tapping a day jumps to that day's session detail (if one exists).
- Needs a legend/tooltip so intensity isn't ambiguous — don't rely purely on color for meaning
  (accessibility principle above).
- This is a custom-built widget (see [09-learning-path.md](09-learning-path.md) item 8) — budget
  real design iteration time, not just implementation time.

## Key screens (rough inventory, refine during Phase 1–2 design)

| Screen | Purpose |
|---|---|
| Onboarding | First-run only: what the app does, get to sign-up fast |
| Login / Sign up | Minimal fields, clear error states |
| Home / Dashboard | Streak, quick "Start Session," today's planned routine if any |
| Routine list | All saved routines, create new |
| Routine editor | Add/reorder/remove exercises, set targets |
| **Active session** | The core screen — logging sets in real time. Must be flawless: fast, thumb-reachable, forgiving of mistakes (easy to edit/undo a just-logged set) |
| Session summary | Shown right after finishing — quick "here's what you did" recap |
| History list | Past sessions, filterable by date |
| Session detail | Full breakdown of a past session |
| Calendar heatmap | The GitHub-style consistency view |
| Exercise detail | Progress chart + PRs + full history for one exercise |
| Profile / Settings | Account, theme, (later) notification preferences |

## Design system

Material 3 (Flutter's default) is the base — it comes with a coherent light/dark theming system
out of the box, which is the lowest-effort path to a consistent look across every screen without
hand-rolling a design system from scratch. Deviate from Material defaults only where the app's
specific needs justify it (the active-session screen and the calendar heatmap are the two most
likely candidates for custom treatment) — not as a general aesthetic preference.

## When in doubt

Favor removing a step over adding an explanation. If a screen needs a tooltip to explain itself,
the first instinct should be "can this be redesigned to not need explaining," and only fall back
to an inline hint if not. This is the practical meaning of "easiest UI" for this app.
