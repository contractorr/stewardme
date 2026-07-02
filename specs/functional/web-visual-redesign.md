---
id: web-visual-redesign
status: implemented
owner: product
last_updated: 2026-07-02
technical_specs:
  - specs/technical/web-visual-redesign.md
  - specs/technical/web.md
---

# Web Visual Redesign (Warm Minimalism)

## Problem

The web app is functional but visually generic and text-heavy in places. Users
see default-looking shadcn surfaces, duplicated controls (two sign-out buttons,
three explanatory paragraphs on the home composer), and no distinctive brand
personality. The goal is a minimalist aesthetic that still feels warm and fun,
and a UI that explains itself with less copy.

## Users

All web app users, on every authenticated page plus the public landing and
login pages. No behavior/API changes — this is a presentation-layer refresh.

## Desired Behavior

1. The whole app shares one "warm minimalism" look: soft warm paper background,
   crisp white cards, a confident amber primary, rounder corners, and a
   distinctive display typeface (Space Grotesk) for the wordmark and page-level
   headings. Body text stays Geist.
2. Chrome is quieter: the top header holds only the mobile menu, wordmark,
   notifications, and settings. Sign-out lives in the sidebar footer only.
3. Sidebar navigation uses a soft rounded "pill" active state in the brand
   color instead of an edge bar, with a solid amber brand tile for the logo.
4. The home page composer keeps its capture/ask auto-detection but shows a
   single, small status hint instead of a badge plus three helper paragraphs.
5. Cards sit flat (hairline border, whisper shadow) and do not lift on hover
   unless a surface is actually clickable. Buttons give a subtle press-down
   micro-interaction so the UI feels responsive and playful.
6. Landing and login pages use the same brand language: display-font hero,
   warm gradient glow, tidy feature grid.

## Acceptance Criteria

- [ ] Light and dark themes both render the new palette; all text/background
      pairs keep readable contrast (muted text ≥ ~4:1 on its background).
- [ ] Header shows no sign-out control; sidebar footer still signs out.
- [ ] Home composer shows exactly one mode-status line; capture/ask
      auto-detection and manual toggle still work unchanged.
- [ ] Wordmark and page hero headings render in the display font; journal,
      chat, and curriculum body content remain in the body font.
- [ ] `npm run lint`, `npm run typecheck`, and `npm run build` pass in `web/`.

## Edge Cases

| Scenario | Expected Behavior |
| --- | --- |
| Display font fails to load | Falls back to Geist/system sans; layout unaffected |
| Lite-mode banner shown | Banner still renders below header, unchanged behavior |
| Dark mode | Same component styles, dark token values; no pure-black surfaces |

## Out of Scope

- Removing or merging product features (see Open Questions — flagged for a
  product decision, not done here).
- Redesigning inner workspace pages (journal, radar, learn, settings) beyond
  what they inherit automatically from shared tokens and components.
- Navigation IA changes.

## Validation Notes

- Smallest meaningful validation slice: `npm run build` + visual pass over
  home, login, landing in light and dark.
- Contract impact: none (no API or data changes).
- Follow-up spec work: per-page polish (journal, radar, learn) can be specced
  separately once this system lands.

## Open Questions

Candidates for future simplification (need product sign-off, intentionally not
done in this change):

- Two settings surfaces exist (SettingsSheet overlay and `/settings` page) —
  consolidating to one would remove a duplicated concept.
- The home composer's manual mode-lock ("Auto/Manual") adds cognitive load;
  auto-detection alone may be enough.
- The landing comparison table (ChatGPT/Notion columns of dashes) is heavy for
  a minimalist page; a short "why StewardMe" list would read better.
