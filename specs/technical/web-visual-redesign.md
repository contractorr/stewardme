---
id: web-visual-redesign
status: implemented
implements:
  - web-visual-redesign
code_paths:
  - web/src/app/globals.css
  - web/src/app/layout.tsx
  - web/src/components/ui/card.tsx
  - web/src/components/ui/button.tsx
  - web/src/components/Sidebar.tsx
  - web/src/components/AppHeader.tsx
  - web/src/app/login/page.tsx
  - web/src/components/landing.tsx
  - web/src/app/(dashboard)/home/page.tsx
test_paths:
  - web/ (lint + typecheck + build)
last_updated: 2026-07-02
---

# Web Visual Redesign — Design System

## Overview

Presentation-layer refresh: OKLCH token overhaul in `globals.css`, a display
font added via `next/font`, flatter cards, press-feedback buttons, and
redesigned chrome (sidebar/header) plus home/login/landing surfaces. No API,
routing, or state changes.

## Dependencies

**Depends on:** Tailwind v4 `@theme inline` tokens, shadcn/ui components,
`next/font/google`.
**Depended on by:** every page under `web/src/app/` (via CSS variables and
shared components).

## Components

### Design tokens (`web/src/app/globals.css`)

**Status:** Stable

#### Behavior

- `--radius` raised 0.625rem → 0.75rem; all shadcn radius steps derive from it.
- Light theme: warm paper background (`oklch(0.982 0.008 90)`), near-white
  cards, warm ink foreground (`oklch(0.235 0.012 50)`), toasted-amber primary
  (`oklch(0.63 0.16 50)`), peach accent, hairline warm borders.
- Dark theme: warm charcoal background, slightly lighter cards, brighter amber
  primary (`oklch(0.78 0.14 55)`) with dark foreground on primary.
- `--font-display` registered in `@theme inline` → exposes a `font-display`
  Tailwind utility. Font stack falls back to Geist then system sans.
- Base layer adds: brand-tinted `::selection`, thin neutral scrollbars
  (WebKit + Firefox), and `text-rendering: optimizeLegibility`.

#### Invariants

- Token names are unchanged — only values change, so every existing
  `bg-card`/`text-muted-foreground`/etc. call site inherits the refresh.
- No component may hardcode raw colors for chrome; use tokens.

### Fonts (`web/src/app/layout.tsx`)

Adds `Space_Grotesk` (`--font-space-grotesk`, subset latin) alongside existing
Geist fonts. Applied only via the `font-display` utility, never globally, so
markdown/curriculum body content keeps Geist.

### Card / Button primitives (`web/src/components/ui/`)

- `card.tsx`: `shadow-sm hover:shadow-md` → `shadow-xs` (flat, no universal
  hover lift). Clickable cards opt into their own hover styles. `CardTitle`
  gains `tracking-tight`.
- `button.tsx`: base gains `active:scale-[0.98]` press feedback (transition-all
  already present). Variants unchanged.

### Chrome (`Sidebar.tsx`, `AppHeader.tsx`)

- Sidebar: active nav item = rounded pill `bg-primary/10 text-primary` (edge
  bar removed); brand tile is solid `bg-primary` with white Brain glyph;
  wordmark uses `font-display`.
- AppHeader: sign-out button removed (sidebar footer keeps it); header is
  `bg-background/80 backdrop-blur` with a soft border.

### Pages (`home`, `login/page.tsx`, `landing.tsx`)

- Home: hero `h1` uses `font-display`; composer keeps mode toggle + detection
  logic but renders one status line (`modeStatus`) instead of the Auto/Manual
  badge and three helper paragraphs. State machine untouched.
- Login: display-font wordmark, solid amber logo tile, same auth flows.
- Landing: display-font hero with radial brand glow, same sections/content.

#### Error Handling

Font download failures at build time fall back per `next/font` behavior;
`font-display` stack includes Geist so runtime rendering degrades gracefully.

## Validation Strategy

- Smallest meaningful test slice: `npm run lint && npm run typecheck &&
  npm run build` in `web/`.
- High-risk regressions to watch: dark-mode contrast, composer mode detection
  on home, mobile sidebar overlay behavior.
