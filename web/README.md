# StewardMe Web App

The `web` workspace contains the Next.js dashboard for StewardMe.

## Stack

- Next.js App Router
- React 19
- Tailwind CSS 4
- `next-auth` for session handling
- Shared FastAPI backend on `http://localhost:8000`

## Local development

```bash
cd web
npm install
npm run dev
```

The frontend expects the API server to be running separately from the repo root:

```bash
uvicorn src.web.app:app --reload --port 8000
```

Open `http://localhost:3000` and sign in.

## Main dashboard areas

- `/` — daily brief and dashboard overview
- `/advisor` — chat and advice flows
- `/goals` — goal tracking, milestones, check-ins, and action plans
- `/journal` — writing, browsing, and filtering journal history
- `/intel` — intelligence feed, trending topics, source health, and saved follow-ups
- `/settings` — API keys, preferences, and account actions

## Goals workspace

The goals page is optimized for active work rather than archival browsing:

- `Focus` shows active and paused goals by default
- `Needs check-in` isolates stale goals that need attention
- `Archived` keeps completed and abandoned goals available without cluttering the main list
- Goal cards support quick status actions: complete, pause, resume, abandon, and reactivate abandoned goals
- Recommendation cards support inline 1-5 rating with optional notes to tune future suggestions
- Search filters the currently loaded goal list by title

## Journal workspace

The journal page is designed for quick retrieval after capture:

- Local search narrows the loaded journal entries by title, preview text, tags, and loaded content
- Type filters help separate daily, project, goal, and reflection entries
- Tag chips give a fast way to pivot into a theme without a dedicated backend search route
- Empty states stay actionable and offer a one-click filter reset
- The composer clarifies that titles are optional and can be auto-generated

## Intel workspace

The radar page is designed for triage, not just passive reading:

- `Trending` highlights cross-source topic convergence
- `Feed` includes quick filters for all items, personalized items, watchlist matches, and saved follow-ups
- Search can be reset in place to return to the recent feed
- Follow-up notes are edited in a side sheet so users can capture next steps without a browser prompt
- Saved items remain available as a lightweight follow-up queue

## Quality checks

```bash
npm run lint
npm run build
```
