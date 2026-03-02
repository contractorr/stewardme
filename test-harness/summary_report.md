# Test Harness Summary Report

**Date:** 2026-03-02
**Sessions:** 6 total (2 per persona across 2 days)
**Personas:** founder (Priya), junior_dev (Alex), switcher (Marcus)

---

## Prioritized Issue List

### P0 — Critical

| # | Issue | Affected | Sessions |
|---|-------|----------|----------|
| 1 | **Onboarding rate limit (429) blocks lite-mode profile completion** — profile interview exhausts lite-mode budget after 1-2 questions. Users can never finish onboarding. Blocks Brief page, prevents profile-based personalization. | founder (both sessions) | 2/6 confirmed, likely all lite-mode users |
| 2 | **Advisor ignores journal context for founder persona** — no RAG retrieval from journal entries despite 2 sessions of content. Advisor treats every question as cold/standalone. junior_dev and switcher get personalization; founder does not. | founder | 2/2 founder sessions |
| 3 | **Radar Feed tab empty (regression)** — Feed shows "Your radar is quiet" / "Run First Scan" while Trending has 212 items. junior_dev session 1 had 50+ feed items; all session 2 runs show empty. `/api/intel/recent` returns 200 but renders nothing. | all 3 personas | 3/3 session-2 runs |

### P1 — High

| # | Issue | Affected | Sessions |
|---|-------|----------|----------|
| 4 | **Sidebar nav links outside viewport** — sidebar items (especially "Conversations") are clipped and unclickable at 900px viewport height. Must navigate via direct URL. | all 3 personas | 5/6 sessions |
| 5 | **Display name uses account name, not onboarding name** — "Good evening, Junior Dev" instead of "Alex", "Switcher" instead of "Marcus". Profile name entered during onboarding is not propagated to dashboard greeting or sidebar. | junior_dev, switcher | all 4 sessions |
| 6 | **Inconsistent onboarding gate** — Brief (`/`) redirects to onboarding when profile incomplete, but Journal, Advisor, and Radar are all accessible. Either gate all pages or none. | founder | 2/2 founder sessions |
| 7 | **Stale conversation 404** — `GET /api/advisor/conversations/{uuid}` returns 404 on first Conversations page load. Conversation ID from a prior session no longer resolves. | all 3 personas | 4/6 sessions |

### P2 — Medium

| # | Issue | Affected | Sessions |
|---|-------|----------|----------|
| 8 | **React hydration mismatches** — Radix UI tab components generate different `aria-controls`/`id` values between SSR and CSR. Console warnings on Radar + Advisor pages. | all 3 personas | 3/6 sessions |
| 9 | **Journal grammar: "1 entries"** — missing singular/plural logic on journal page header. | founder | confirmed in screenshots |
| 10 | **Journal card shows raw markdown** — `##` headers render as plaintext in card preview instead of stripped/rendered text. | founder | 2/2 sessions |
| 11 | **Brief page flash of empty content** — renders empty `<main>` before redirecting to `/onboarding`. Should redirect server-side or show loading. | founder | 2/2 sessions |
| 12 | **Journal dialog stays open after save** — form resets (type reverts to Daily) but dialog doesn't close. Minor friction. | switcher | 1/6 sessions |
| 13 | **Next.js "1 Issue" dev badge visible** — bottom-left debug badge visible in what should be production UI. | junior_dev, founder | 2/6 sessions |

### P3 — Low

| # | Issue | Affected | Sessions |
|---|-------|----------|----------|
| 14 | **Radar topic toggle UX** — during onboarding, pre-selected topics toggle off on click with no clear selected/unselected visual state. | switcher | 1/6 sessions |
| 15 | **Radar Feed has no pagination** — 50+ items in a single scroll with no infinite-scroll indicator or load-more. | junior_dev | session 1 only (feed now empty) |
| 16 | **Advisor response time ~60s in lite mode** — only "Thinking..." text shown, no progress indicator. Acceptable but noticeable. | junior_dev | session 2 |

---

## Common Bugs Across Personas

**Universal (all 3 personas):**
- Sidebar nav links outside viewport (layout/CSS)
- Radar Feed empty in session 2 (regression)
- Stale conversation 404 on Conversations page load
- Hydration mismatch warnings (Radix UI)

**2 of 3 personas:**
- Display name mismatch (junior_dev, switcher — founder never completed onboarding)
- Next.js dev badge visible (junior_dev, founder)

**Founder-only:**
- Onboarding 429 rate limit (lite mode)
- No journal-based personalization in advisor
- Inconsistent onboarding page gating
- Grammar and raw markdown in journal cards

---

## UX Patterns

### What works well
- **Onboarding interview** — conversational, adaptive questioning. Feels like a coaching intake, not a form. Auto-generates specific goals from answers (junior_dev got 3, switcher got 5). Standout first-time experience when it completes successfully.
- **Journal entry creation** — clean dialog with title/type/tags/content. Toast confirmation. Cards render in a nice grid. Entries persist across sessions.
- **Advisor response formatting** — well-structured with section headers, bullet points, bold emphasis, nested lists. Ends with follow-up questions that encourage return usage.
- **Radar Trending view** — clustered topics with summaries, source attribution badges, expandable items, "For you" personalization tags with match reasons (skill:data, goal:own). Best-designed page in the app.
- **Lite mode banner** — persistent, informative, non-intrusive. Clear CTA to add API key.
- **Dashboard suggested questions** — contextual to user's goals, good engagement nudge.

### What needs work
- **Onboarding + lite mode** — rate limit kills the flow immediately. The very first interaction fails. Users told to "add your own API key" during first-time setup — hostile first-run experience.
- **Feed vs Trending disconnect** — two tabs on the same page showing contradictory states (212 items vs "nothing yet"). Confusing mental model. Users who discover Feed first think the system has no data.
- **Sidebar responsiveness** — at 900px height, nav items are clipped. No scroll, no overflow handling. Users can't reach "Conversations" without direct URL.
- **Profile data propagation** — name entered in onboarding doesn't reach dashboard greeting or sidebar. Feels like the system didn't remember you.
- **Journal previews** — raw markdown in card text (## headers visible). Should either render or strip formatting markers.
- **Empty states** — Brief shows empty `<main>` flash. Feed says "I haven't scanned anything yet" when data exists. Inconsistent messaging.

---

## Advisor Quality Trends

### Session 1 → Session 2 comparison

| Persona | Session 1 | Session 2 | Trend |
|---------|-----------|-----------|-------|
| **founder** | High quality, generic. Well-structured competitive advice. No profile or journal context. | High quality, still generic. No RAG retrieval despite 2 journal entries. Good structure but zero personalization. | **Flat** — quality stays high but no adaptation |
| **junior_dev** | Strong first session. Referenced profile data from onboarding. Gave relevant career advice. Personalization 4/5. | Excellent. Referenced journal entry about PR review, linked to existing goals, gave specific response scripts. Personalization 5/5. | **Improving** — clear cross-context reasoning in session 2 |
| **switcher** | Exceptional for first session. Referenced SEC filings project, Python level, imposter syndrome, time constraints. Gave honest pushback. | Even better. Phased learning plan with per-item hour budgets totaling 288hrs (12h/wk x 6mo). Specific resource recommendations. Explicit "skip list." | **Improving** — more specific, opinionated, and actionable |

### Key observations

1. **Personalization divergence by persona**: junior_dev and switcher show strong and improving personalization. founder shows none — likely because the profile interview never completed (429 error), so no profile exists for RAG retrieval. This is the onboarding rate limit bug manifesting as a downstream quality problem.

2. **Baseline quality is high even without personalization**: founder's advisor gave genuinely useful strategic advice both sessions despite having zero user context. The default prompt engineering and Haiku model produce solid outputs.

3. **Journal→advisor pipeline works when profile exists**: junior_dev session 2 proved the system can reference journal entries in advisor responses ("your journal says you want backend fundamentals"). switcher session 2 showed SEC field-level detail pulled from profile context. The RAG pipeline works — the founder is the outlier due to missing profile.

4. **Cross-conversation continuity is weak**: No persona's advisor referenced prior conversations. Each new conversation starts fresh. Session 1 advisor conversation is not carried into session 2 context.

5. **Tone calibration is good**: Each persona got appropriate tone — direct/strategic for founder, empathetic/practical for junior_dev, structured/mentoring for switcher. The system adapts tone well even across lite mode.

---

## Aggregate Scores

| Category | Founder S1 | Founder S2 | Junior S1 | Junior S2 | Switcher S1 | Switcher S2 | **Avg** |
|----------|-----------|-----------|----------|----------|------------|------------|---------|
| Functionality | 4 | 4 | 5 | 4 | 5 | 4 | **4.3** |
| Personalization | 2 | 2 | 4 | 5 | 4 | 5 | **3.7** |
| Adaptation | N/A | 2 | 3 | 4 | N/A | 4 | **3.3** |
| UX | 4 | 3.5 | 4 | 4 | 4 | 4 | **3.9** |

**Overall: 3.8/5** — functional and well-designed, dragged down by the onboarding/personalization gap for lite-mode users and the Feed regression.

---

## Recommendations

1. **Fix lite-mode onboarding budget** — either exempt profile interview from rate limit, batch interview into fewer LLM calls, or pre-fill profile from a shorter form. This is the highest-leverage fix: it unblocks Brief, enables personalization, and fixes the founder persona entirely.

2. **Fix Radar Feed regression** — Feed and Trending query different endpoints/data paths. Unify them or ensure Feed's `/api/intel/recent` actually returns the global intel data that Trending clusters from.

3. **Fix sidebar overflow** — add `overflow-y: auto` or collapsible nav for shorter viewports. All three personas hit this.

4. **Propagate onboarding name to dashboard/sidebar** — use the name from profile interview as display name, falling back to account name.

5. **Investigate cross-conversation context** — advisor starts fresh each conversation. Consider injecting a summary of recent conversations or linking conversation history to RAG retrieval.

6. **Clean up hydration mismatches** — Radix UI tabs need stable IDs across SSR/CSR. Use `useId()` or suppress hydration for those components.
