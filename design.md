# Design — csl-portfolio

The locked design system for the portfolio site. Every page redesign reads this
file before writing code. Extend or amend it when the system needs to grow; do
not invent a new system per page. The rationale and the page-by-page plan are in
`docs/frontend-redesign-spec.md`.

**Out of scope:** the three A4 sheets on `/resume` (`components/resume/*`) are
matched to the official PDF and keep their own `brand.*` colours and layout.

## Genre
modern-minimal — restrained, precise, an engineer's and researcher's tool
aesthetic. Hairline rules carry structure instead of shadows. No decorative
gradients, no glassmorphism, no gradient text.

## Macrostructure family
- Marketing pages (`/`): Split Studio — H2 split diptych (claim + CTAs left,
  F3 ruled spec sheet right), then an asymmetric routing block.
- Content pages (`/projects`): editorial case — featured project as a two-column
  case (main + spec side column), the rest as an F3 ruled index.
- App pages (`/agents`): Workbench — a ruled status strip above one flat
  conversation surface. No card-in-card.
- Utility (`/resume` toolbar, `/resume/ats`, 404): a single ruled bar or block.

Nav: **N5 Floating pill** (sticky, content-sized, detached from the edges).
Footer: **Ft2 Inline single line** (hairline rule above, credit left, links right).

## Theme
Custom OKLCH palette anchored on the existing cool blue (H ≈ 242).
- `--color-paper`          oklch(97.2% 0.006 242) — page
- `--color-paper-2`        oklch(99.2% 0.003 242) — surfaces
- `--color-surface-subtle` oklch(94.2% 0.011 242) — hover, agent replies
- `--color-ink`            oklch(22% 0.02 250) — text, filled buttons (15.96:1 on paper)
- `--color-ink-2`          oklch(46% 0.02 248) — secondary text (6.56:1 on paper)
- `--color-rule`           oklch(87% 0.014 242) — hairlines (decorative only, 1.45:1)
- `--color-rule-strong`    oklch(62% 0.02 245) — form control borders
- `--color-accent`         oklch(48% 0.12 245) — text links (5.99:1 on paper)
- `--color-focus`          oklch(48% 0.12 245) — focus ring
- Status pairs: live 8.07:1, soon 6.82:1, muted 5.79:1. Danger 6.45:1 on paper-2.

Accent is for links and the focus ring only — never large fills.

## Typography
- Display: Space Grotesk 700 (500 available), roman only, tracking −0.015 to −0.03em
- Body:    Noto Sans TC 400 / 500 (Microsoft JhengHei, PingFang TC fallbacks)
- Mono:    JetBrains Mono 400 / 500 — years (`tabular-nums`), `<code>`, stack tags, agent names
- Display anchor: `clamp(2.75rem, 6vw + 1rem, 5rem)` on the home headline only

## Spacing
4-point scale in `tokens.css` (`--space-3xs` 0.25rem … `--space-2xl` 4.5rem).
Pages use Tailwind arbitrary `rem` values on the same steps. No `px` except
1px hairlines.

## Motion
- motion-cut: no animation library, no scroll reveals.
- Transitions name the property (`transition-colors`), 180 ms, `--ease-out`
  cubic-bezier(0.16, 1, 0.3, 1).
- `prefers-reduced-motion: reduce` removes transitions and the press offset.

## Microinteractions stance
- Focus ring is instant: 2px `--color-focus`, offset 2px, never transitioned.
- Press: `active:translate-y-px` on buttons and button-like links.
- Silent success; errors render inline in `--color-danger` with `role="alert"`.
- Clickable text never wraps (`whitespace-nowrap`).

## CTA voice
- Primary: filled ink pill, `--color-on-ink` text, short verb phrase (查看履歷).
- Secondary: paper pill with a `--color-rule-strong` border (瀏覽專案).
- Inline: accent text link with a trailing → or ↗, underline on hover.

## Per-page allowances
- No hero imagery or enrichment on any page; typography carries the site.
- Eyebrow kickers are off everywhere.

## What pages MUST share
- The `Spark.dev` wordmark in the N5 pill and the Ft2 footer.
- The palette, the three faces, the CTA voice and the focus ring.
- Hairline rules (`--color-rule`) as the structural divider.

## What pages MAY differ on
- Macrostructure within the family above.
- Whether a block uses a ruled list or a single bordered surface.

## Exports

### tokens.css
The canonical file is `apps/web/src/styles/tokens.css`, imported first by
`apps/web/src/styles/main.css` and mapped into Tailwind colour and font names in
`apps/web/tailwind.config.ts`.
