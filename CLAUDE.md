# csl-portfolio — Agent Guide

Personal portfolio for 廖啓舜 (Spark): résumé, projects, and AI-agent playground.
Monorepo with a Vue 3 SPA (`apps/web`, pnpm) and a FastAPI backend (`apps/api`, uv).
Full architecture: `docs/architecture.md`. Deploy pipeline: `docs/deploy-cloudrun.md`.

## Layout

```
apps/web/src/
  pages/        Home / Resume / AtsResume / Projects / Agents / NotFound
  components/   resume/* (ProfileCard, SidebarPanel, ExperienceCard, ResumeSheet …), ui/*
  composables/  useDownload (PDF/PNG export), useChat, useFitScale (A4 → phone)
  data/         resume.ts (履歷內容), projects.ts (專案作品) — all copy lives here
  types/        resume.ts, project.ts
apps/api/server/  FastAPI app: routes/, agents/ (registry + BaseAgent), integrations/line_client
docs/             架構、部署、履歷規則
```

## Commands (run from the repo root)

```bash
pnpm install                 # web deps (Node ≥ 22, pnpm via packageManager)
uv sync --project apps/api   # api deps
pnpm dev:web / pnpm dev:api  # Vite on 5173 proxies /api → uvicorn on 8000
pnpm check                   # type-check + lint:web + test:web + lint:api + test:api
pnpm build:web               # vue-tsc -b && vite build
pnpm typecheck:api           # mypy --strict
```

Run `pnpm check` before committing. CI (`.github/workflows/ci.yml`) runs the same
set plus `ruff format --check` and the web build; `deploy-cloudrun.yml` ships `main`.

## Web conventions

- Tailwind with arbitrary values in `rem` (`px-[1.25rem]`), brand tokens from
  `tailwind.config.ts`: `brand-start #76abd6`, `brand-end #8ebfe5`,
  `brand-sidebar #e8edf3`, `brand-page #edf1f5`, `brand-ink #1f2633`, `brand-muted #4a5568`.
- Font stack: `"Noto Sans TC", "Microsoft JhengHei", "PingFang TC", "Segoe UI", sans-serif`.
- Cards: white, radius 1.25–1.75 rem, `shadow-card`; section kicker in tracked uppercase.
- Chinese copy uses full-width punctuation（，；：（））. `src/data/content.test.ts`
  fails on half-width marks next to CJK characters.
- New page = route in `router/index.ts` (with `meta.title`) + link in `components/ui/AppNav.vue`
  + card on `HomePage.vue` if it is a top-level section.
- Heavy libraries (html2canvas, jsPDF) are dynamically imported; keep the resume
  page chunk small.
- No runtime config is baked into the bundle; nginx `envsubst` injects it at container start.

## Resume rules (`/resume`)

- Three fixed A4 sheets (`.resume-page`, 210 mm × min 297 mm). `ResumeSheet.vue`
  scales them down on narrow screens; export and print always use scale 1.
- **Page 1 has the least slack.** After changing `resume.ts` or any resume
  component, render `/resume` in headless Chromium at 1200 × 1697 with a Noto
  Sans CJK font available and confirm every `.resume-page` is still 297 mm
  (≈1122.5 px) tall. If page 1 grows, tighten spacing or shorten the new bullet;
  do not let it spill.
- Keep wording identical to the PDF source (`apps/web/public/廖啓舜_履歷.pdf`)
  unless the user supplies new copy. Tools render as one `、`-joined line.
- Page numbers: `01`–`03`, letter-spaced, bottom-right, plain text.
- The ATS version (`/resume/ats`) derives from the same data; it has no page limit.
- Headshot in `public/profile.jpg` is served at 150 px (300 px on 2× export); keep it ≤ ~800 px wide.

## Data / privacy

- `archive/`, `reference/`, `assets/`, `docs/my*.md`, `docs/resume_自傳.md` are gitignored
  personal material. Never commit `.env`; `.env.example` documents the keys.
- Contact details in `resume.ts` are public by the user's choice; do not add others.

## Terminal preference

The user works on Windows with Git Bash. When a tool runs shell commands on their
machine, wrap them as `bash -c "..."` rather than PowerShell unless PowerShell is required.
