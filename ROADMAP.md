# Roadmap

This is the **narrative** view of where the project is going. For the contributor-facing plan with concrete epics, issues, and difficulty tags, see [PLAN.md](PLAN.md). The authoritative, up-to-date view is the [GitHub Project board](https://github.com/sausi-7/a0-angular/projects).

## Phase 0 — Foundation (current)

Repo skeleton, CI, docker-compose, governance docs. No features yet.

**Exit:** A contributor can clone, `make dev`, and see both services healthy.

## Phase 1 — MVP: generate + preview

One-shot generation of a small Angular app from a prompt, with a live iframe preview.

- `POST /projects` accepts a prompt, streams LLM output over WebSocket
- Agent loop with three tools: `write_file`, `read_file`, `run_ng_generate`
- System prompt encodes Angular 19 conventions
- Web UI: chat, streaming file-diff view, Monaco (read-only), preview iframe
- BYOK settings screen; keys encrypted at rest

**Exit:** "Build me a todo app with local storage" → working preview in <2 minutes.

## Phase 2 — Iterative editing

- Multi-turn chat per project
- `edit_file` tool with structured search/replace diffs
- File tree with click-to-open Monaco
- Undo/redo via auto-commits; "revert to checkpoint" UI
- Error-aware loop (feed `ng serve` / tsc errors back to the agent)

## Phase 3 — Multi-user & auth

- `fastapi-users` with email/password + GitHub OAuth
- Postgres via Alembic migrations
- Per-user project isolation
- Per-user, per-provider rate limits
- Redis + `arq` for background jobs

## Phase 4 — Richer editing surface

- Visual component selector (click in preview → agent gets component path)
- Design-token editor (Tailwind config, CSS vars)
- `npm add` tool with allowlist
- Template gallery (auth, dashboard, CRUD)

## Phase 5 — Deployment & sandbox options

- One-click deploy: Vercel / Netlify / Cloudflare Pages / Fly.io / Railway
- Pluggable sandbox interface (local, Docker-per-project, E2B)
- Push generated project to user's GitHub
- Self-hosted install docs for Hetzner / DigitalOcean

## Phase 6+ — Community-driven

Surface votes on the Project board. Candidates: visual drag-drop builder, Angular Material / PrimeNG / Spartan pickers, Storybook-per-project, a11y linter, i18n scaffolding.

## How to influence the roadmap

- 👍 on the GitHub issue that tracks the feature
- Comment with your use case
- Open a new discussion if your need isn't tracked
- Send a PR — code speaks loudest
