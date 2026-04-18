# Project Plan

This is the contributor-facing plan for A0 for Angular. It is more concrete than [ROADMAP.md](ROADMAP.md): each phase lists *epics* (parallelizable workstreams) and inside each epic a punch list of *issues* a contributor can pick up.

If you want to help build this into the de-facto Angular vibe-coding platform, this is the document to read.

---

## How to read this plan

- **Phases run sequentially.** A phase is "done" when its exit criteria are met. We do not start the next phase until the current one ships.
- **Epics inside a phase run in parallel.** Pick the one that matches your skills.
- **Issues** are the unit of work. Each issue is sized to fit in one PR (~1–3 days for an experienced contributor).
- **Difficulty tags:**
  - `D1` — good first issue. Self-contained, well-specified, no deep context needed.
  - `D2` — intermediate. Requires understanding one subsystem; mentorship available in the linked GitHub issue.
  - `D3` — advanced. Touches the agent loop, security boundary, or cross-cutting infra; expect design discussion before code.
- **Claiming work.** Comment "I'd like to take this" on the GitHub issue. A maintainer will assign within 48h. If we don't respond, ping in Discussions.
- **Definition of done** for every issue: code + tests + docs updated + `make lint test` green.

---

## Current status

- **Phase 0:** complete (this repo).
- **Phase 1.0 — Demo-ready vertical slice:** open. **Start here if you want the fastest path to "it works."** This is the ~12-issue subset of Phase 1 that produces the launch-day demo gif.
- **Phase 1 (full MVP):** open for contribution in parallel with Phase 1.0. Pick from any epic.
- Phases 2+ are scoped here so contributors can see the trajectory, but their issues are not yet filed. We file them as the previous phase nears exit.

---

## Phase 0 — Foundation [complete]

Repository skeleton, CI, governance, contributor docs.

**Delivered:**
- Monorepo: `apps/web` (Angular 19), `apps/api` (FastAPI), `packages/{agent-core, ng-schematics, shared-types}`
- CI: lint, typecheck, test, build for both stacks
- CodeQL security scanning
- Dependabot for npm, pip, GitHub Actions
- Governance: README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CODEOWNERS, PR + issue templates
- Architecture docs and ADRs 0001–0003
- `make dev` runs both services natively; `make dev-docker` runs them via compose

**Exit criterion (met):** a contributor can clone, run `make install && make dev`, and see both services healthy at :4200 and :8000.

---

## Phase 1.0 — Demo-ready vertical slice

> The smallest possible cut across agent / API / web / sidecar that produces the launch-day demo gif. Everything not on the gif is deferred to Phase 1 proper.

**Goal:** record a 30-second screen capture of `prompt → streamed file changes → working Angular preview in iframe`. Single user, single project, single provider, single happy-path prompt ("Build me a todo app with localStorage").

**Exit criteria:**
1. `make dev` plus `ANTHROPIC_API_KEY=…` in `.env` is the entire setup.
2. The configured prompt produces a runnable todo app in `workspace/demo/` with a working preview at the iframe URL.
3. A `docs/media/demo.gif` is committed and embedded in the README.
4. No regression in CI.

**Aggressive cuts (deferred to full Phase 1):** BYOK UI, multiple providers, Monaco, file tree, project picker, multi-turn chat, `edit_file`, `run_ng_generate`, SQLite persistence, settings encryption, Playwright, OpenAPI codegen, Dockerfile updates, structured logging.

**Cuts in detail:**
- One provider only (Anthropic). Key from env, not DB.
- One project, fixed id `demo`, fixed sidecar port `4300`.
- Two tools only: `write_file` and `read_file`.
- In-memory project state (dict). No DB.
- Pre-seeded Angular starter copied into the workspace at first run, so `ng serve` boots in ~3s instead of `ng new`'s ~60s.

| # | Issue | Difficulty | Notes |
|---|---|---|---|
| 1.0.1 | `LLMProvider` ABC + `AnthropicProvider` (streaming + tool use, env-var key) | D2 | Minimal surface — single class, no factory. |
| 1.0.2 | Tool: `write_file(path, content)` with workspace-root path validation | D2 | Reuse-ready in full Phase 1; same code. |
| 1.0.3 | Tool: `read_file(path)` with 256 KB cap | D1 | Same as 1.1.7 in the full plan. |
| 1.0.4 | Agent loop runner: provider + tool dispatch + event emit | D2 | No token-budget trimming, no conversation persistence. |
| 1.0.5 | System prompt for the todo-app happy path | D1 | `prompts/system_demo.md`. Tight, one task, no branching. |
| 1.0.6 | `POST /demo/start` — copy starter template into `workspace/demo/`, return readiness | D1 | Idempotent: re-running wipes and re-seeds. |
| 1.0.7 | `WS /ws/demo` — receive `{prompt}`, run agent, stream events | D2 | One inbound message; many outbound events. |
| 1.0.8 | Sidecar manager (single instance): spawn `ng serve --port 4300`, kill on shutdown | D2 | Lifecycle tied to API process; `atexit` cleanup. |
| 1.0.9 | Web shell: two-pane layout — left prompt + event log, right preview iframe | D1 | Tailwind, no splitter. |
| 1.0.10 | WebSocket client service that connects to `/ws/demo` and pushes events into a Signal | D2 | No reconnect logic; refresh on disconnect. |
| 1.0.11 | Preview iframe: poll `localhost:4300/` until 200, then load | D1 | Show "preview booting…" until ready. |
| 1.0.12 | Bundle starter Angular template in `packages/templates/demo-starter/` + record `docs/media/demo.gif` | D2 | The gif is the deliverable. |

**How a single contributor could ship this:** 1.0.1 → 1.0.2 → 1.0.3 → 1.0.4 → 1.0.5 (backend agent works against `workspace/demo/` from a python script). Then 1.0.6 → 1.0.7 → 1.0.8 (API + sidecar). Then 1.0.9 → 1.0.10 → 1.0.11 (web). Then 1.0.12 (template + gif). Realistic solo timeline: 2–3 focused weekends.

**After Phase 1.0 ships,** post the launch on r/Angular with the gif. Then continue with full Phase 1 in parallel — every Phase 1.0 issue's code becomes the foundation for its Phase 1 counterpart, not throwaway.

---

## Phase 1 — MVP: Prompt → Working Angular App

> The single most important phase. After Phase 1, A0 does the thing it claims to do: a user types a prompt, watches files stream in, and sees a working Angular app preview.

**Goal:** "Build me a todo app with localStorage" → preview renders a working app in under 2 minutes, end-to-end.

**Exit criteria:**
1. User can submit a prompt via the web UI and see streamed file writes land in `workspace/<project>/`.
2. A sidecar `ng serve` boots the generated project and renders it in the preview iframe.
3. The full loop works with at least one BYOK provider (Anthropic).
4. There is an E2E test that drives the loop headlessly and asserts the preview returns 200.
5. The flow is documented in [docs/architecture.md](docs/architecture.md) and a 90-second demo gif is in the README.

**Non-goals for Phase 1:** auth, multi-user, edit-after-generate (that is Phase 2), Docker sandboxing, deployment.

### Epic 1.1 — Agent core (`packages/agent-core`)

The provider-agnostic loop that streams tokens and executes tool calls.

| # | Issue | Difficulty | Notes |
|---|---|---|---|
| 1.1.1 | Define `LLMProvider` interface (Pydantic) and event types | D2 | Events: `token`, `tool_call`, `tool_result`, `file_changed`, `error`, `done`. Document in `agent-core/README.md`. |
| 1.1.2 | Implement `AnthropicProvider` with streaming + tool use | D2 | Use the official `anthropic` SDK. Cite [docs/adr/0002-byok.md](docs/adr/0002-byok.md) for key handling. |
| 1.1.3 | Implement `OpenAIProvider` | D2 | Mirror 1.1.2. |
| 1.1.4 | Implement `OpenRouterProvider` | D2 | Same surface, different base URL + model strings. |
| 1.1.5 | Tool registry with `@tool` decorator and Pydantic arg schemas | D3 | Tools self-register; the loop introspects to build provider-specific tool schemas. |
| 1.1.6 | Tool: `write_file(path, content)` with workspace-root path validation | D2 | Reject `..`, absolute paths, symlinks. |
| 1.1.7 | Tool: `read_file(path)` with size cap | D1 | 256 KB cap; return UTF-8 with a clear error on binary. |
| 1.1.8 | Tool: `run_ng_generate(schematic, name, options)` shelling to Angular CLI | D2 | Lives in `packages/ng-schematics`; agent-core imports it. |
| 1.1.9 | Conversation state: messages + tool results, with token-budget trimming | D2 | First-pass: trim oldest non-system messages when over budget. |
| 1.1.10 | System prompt encoding Angular 19 conventions | D1 | Standalone components, Signals, new control flow. Lives in `packages/agent-core/prompts/system_angular.md`. |
| 1.1.11 | Unit tests with a `FakeProvider` (deterministic responses) | D2 | Lets us test the loop without API calls. |

### Epic 1.2 — API surface (`apps/api`)

| # | Issue | Difficulty | Notes |
|---|---|---|---|
| 1.2.1 | `POST /projects` — create project, allocate workspace dir + sidecar port | D1 | Returns `{id, workspace_path, preview_port}`. |
| 1.2.2 | `GET /projects` and `GET /projects/{id}` | D1 | List and detail. |
| 1.2.3 | `WebSocket /ws/projects/{id}` — receives prompt, forwards agent events | D3 | Single message in, many events out. Backpressure-aware. |
| 1.2.4 | `GET /projects/{id}/files` and `/files/{path}` — read-only file access | D2 | For Monaco. |
| 1.2.5 | SQLAlchemy 2.0 async models: `Project`, `Message`, `Setting` | D2 | SQLite via `aiosqlite`. |
| 1.2.6 | Settings endpoints for BYOK keys (encrypted column) | D2 | `cryptography.Fernet` keyed off `A0_SECRET_KEY`. |
| 1.2.7 | Structured logging (JSON, no secrets) | D1 | `structlog`. |
| 1.2.8 | OpenAPI export script feeding `packages/shared-types` codegen | D2 | `python -m app.export_openapi` + CI step. |

### Epic 1.3 — Web UI (`apps/web`)

| # | Issue | Difficulty | Notes |
|---|---|---|---|
| 1.3.1 | Three-pane layout: chat (left), preview (right), file diff (overlay) | D2 | Tailwind, Signals. |
| 1.3.2 | Chat input + message list with streaming token rendering | D2 | `@for` over a Signal of messages; append tokens without re-render churn. |
| 1.3.3 | WebSocket service that subscribes to `/ws/projects/{id}` events | D2 | Reconnect with backoff. |
| 1.3.4 | File diff overlay that animates each `file_changed` event | D2 | Show before/after; auto-dismiss after N seconds. |
| 1.3.5 | Preview iframe pointing at sidecar `ng serve` port | D1 | Sandbox attributes; reload-on-stale-port. |
| 1.3.6 | Monaco editor (read-only) for clicked file in tree | D2 | Lazy-load monaco to keep initial bundle small. |
| 1.3.7 | BYOK settings screen: provider, model, key (masked) | D2 | Posts to API; never logs the key client-side either. |
| 1.3.8 | Project picker / new-project flow | D1 | Persists last-opened project in localStorage. |

### Epic 1.4 — Sidecar `ng serve` manager

| # | Issue | Difficulty | Notes |
|---|---|---|---|
| 1.4.1 | Process supervisor: spawn / kill / restart `ng serve` per project | D3 | Allocate a port from a pool; clean up on project delete. |
| 1.4.2 | Health probe (`GET http://localhost:<port>/`) before unblocking the iframe | D2 | Surface "preview booting" state to the UI. |
| 1.4.3 | Capture sidecar stderr; forward compile errors as agent events | D2 | Foundation for Phase 2's error-feedback loop. |

### Epic 1.5 — End-to-end testing

| # | Issue | Difficulty | Notes |
|---|---|---|---|
| 1.5.1 | Playwright setup in CI | D2 | Headless Chrome. |
| 1.5.2 | E2E: "build me a hello-world component" using the `FakeProvider` (no real LLM call) | D2 | Asserts preview responds 200. |
| 1.5.3 | Smoke test: real Anthropic call gated on a CI secret, runs nightly | D3 | `vcr.py`-style cassettes for replay. |

---

## Phase 2 — Iterative Editing & Error Recovery

> Phase 1 generates. Phase 2 makes generation usable: edit existing projects, recover from compile errors automatically, and let users undo bad turns.

**Exit criteria:**
1. User can have a multi-turn conversation against an existing project; the agent produces structured diffs (not full-file rewrites).
2. When `tsc` or `ng serve` errors, the agent receives them and produces a fix without user intervention.
3. Every agent turn produces a git commit in the project workspace; user can revert to any prior turn from the UI.
4. Token-cost meter is visible per-message and per-project.

### Epic 2.1 — Structured edits

- `edit_file` tool: takes `(path, old_str, new_str)` blocks; rejects ambiguous matches.
- File diff renderer in UI uses the same blocks (no client-side guessing).
- Multi-edit batching to keep token cost down.

### Epic 2.2 — Error-feedback loop

- Subscribe to sidecar tsc / `ng serve` output.
- On error, build a synthetic user message: "Last build failed with: <error>. Fix and try again."
- Cap to N retries; surface to user after the cap.

### Epic 2.3 — Checkpointing

- Auto-init git repo in each project workspace.
- Commit after every successful agent turn with the user prompt as the message.
- "Revert to checkpoint" UI maps to `git reset --hard <sha>`.

### Epic 2.4 — Context compression

- Summarize older turns when conversation exceeds a token budget.
- Pluggable summarizer (default: smaller model from same provider).

### Epic 2.5 — Cost & telemetry

- Per-message token + USD estimate.
- Project-level cost dashboard.
- Anonymous usage telemetry (opt-out, documented).

---

## Phase 3 — Multi-user, Auth, and Hosted-Ready

> Until Phase 3, A0 is single-user / self-host-only. Phase 3 makes it possible to host A0 for many users.

**Exit criteria:**
1. Email/password and GitHub OAuth sign-in.
2. Per-user project isolation enforced at the data and filesystem layers.
3. Postgres backend with Alembic migrations.
4. Background jobs (sidecar lifecycle, cleanup, cost rollups) on Redis + `arq`.
5. Per-user, per-provider rate limits.

### Epic 3.1 — Auth

- `fastapi-users` integration.
- GitHub OAuth via `httpx-oauth`.
- JWT access + refresh tokens.
- "Sign in" / "Sign up" / "Account" screens.

### Epic 3.2 — Postgres + migrations

- SQLAlchemy already async; swap dialect.
- Alembic with autogenerate hooks.
- Migration test in CI: "fresh DB → all migrations apply → schema matches models".

### Epic 3.3 — Tenancy

- Every query scoped by `user_id`; enforce in a base repository class.
- Workspace dirs scoped by `user_id`.
- Audit log for sensitive actions (key add/remove, project delete).

### Epic 3.4 — Background jobs

- Redis + `arq` worker.
- Move sidecar supervision off the request thread.
- Idle-project reaper.

### Epic 3.5 — Rate limiting & abuse controls

- Per-user, per-provider request budget.
- IP-based throttling at the WebSocket entry.
- Honeypot for sign-up to deter scripted abuse.

---

## Phase 4 — Richer Editing Surface

> Phase 4 makes A0 feel like a design tool, not just a chat box.

**Exit criteria:**
1. Click any element in the preview iframe → the agent gets the component path + element selector.
2. Design tokens (colors, spacing, font) editable in a side panel; changes propagate via Tailwind config.
3. `npm add` tool with maintainer-curated allowlist.
4. Template gallery: at least 5 starters (auth, dashboard, CRUD, landing, blog).

### Epic 4.1 — Visual selection bridge

- Inject a small script into the preview iframe that captures clicks and posts the source-map-resolved path back to the parent.
- Pre-populate next prompt with `In <component>:line, …`.

### Epic 4.2 — Design-token editor

- Read/write a single `tokens.json` in the project.
- Live-update Tailwind config and theme CSS vars.
- Color-contrast warnings.

### Epic 4.3 — Package management

- Curated allowlist (`packages/agent-core/allowlist.json`) of npm packages the agent can install.
- `npm add` tool guarded by allowlist + max-deps cap.
- PR-via-bot to add packages to the allowlist.

### Epic 4.4 — Template gallery

- "Start from template" flow.
- Each template lives in `packages/templates/<name>/` with a manifest.
- Initial templates: `auth`, `dashboard`, `crud`, `landing`, `blog`.

---

## Phase 5 — Deployment, Sandboxing, Hardening

> Phase 5 makes generated projects shippable and the platform itself production-ready.

**Exit criteria:**
1. One-click deploy to at least 3 of: Vercel, Netlify, Cloudflare Pages, Fly.io, Railway.
2. Pluggable `SandboxBackend` with `Local`, `Docker`, and `E2B` implementations.
3. "Push to GitHub" flow that creates a repo under the user's account.
4. Production install guide for Hetzner and DigitalOcean with reverse proxy + TLS.
5. Observability: OpenTelemetry traces and metrics shipped to a default OTLP endpoint.

### Epic 5.1 — Deploy adapters

- One adapter per target: `VercelDeployer`, `NetlifyDeployer`, etc.
- OAuth-per-target stored in user settings.
- Deployment logs streamed to the UI like agent events.

### Epic 5.2 — Sandbox abstraction

- `SandboxBackend` interface: `start`, `stop`, `read`, `write`, `exec`.
- `LocalSandbox` (Phase 1 default) → factor out behind the interface.
- `DockerSandbox` — one container per project; enforced CPU/mem limits.
- `E2BSandbox` — for hosted multi-tenant setups.

### Epic 5.3 — GitHub push

- OAuth scope: `repo` (warn on first use).
- Create repo + initial push from project workspace.
- Optional: open a PR back from a "remix" of someone else's published template.

### Epic 5.4 — Self-host docs

- Step-by-step Hetzner / DO guide with `caddy` reverse proxy.
- Environment-variable reference page.
- Backup & restore guide.

### Epic 5.5 — Observability

- OpenTelemetry SDK in API.
- Structured event stream to OTLP.
- Reference Grafana dashboard JSON in `docs/observability/`.

---

## Phase 6 — Community Surface

> Phase 6 turns A0 into a platform other people build on.

**Exit criteria:**
1. Plugin system: third parties can publish providers, sandbox backends, and tools as installable npm/pip packages discovered at runtime.
2. Public template registry where the community submits templates via PR.
3. Spartan / Material / PrimeNG starter packs picked at project creation.
4. Per-project Storybook that the agent can populate.
5. a11y linter ships with every generated project; warnings surface in the chat panel.
6. i18n scaffolding: `@angular/localize` wired in, translation extraction documented.

### Epic 6.1 — Plugin system

- Discovery via entry points (Python) and `package.json` keywords (npm).
- Sandbox: plugins run in a subprocess, not in the main API process.
- Plugin metadata schema + signature verification.

### Epic 6.2 — Template registry

- `templates.a0-angular.dev` static site listing community templates.
- PR-to-add workflow with automated checks (builds, passes a11y, no postinstall scripts).

### Epic 6.3 — UI library packs

- Project-creation step: "Pick a UI library."
- One pack per library: starter components, agent prompts, allowlist additions.

### Epic 6.4 — Storybook integration

- `add_storybook` tool the agent can call.
- Auto-generate stories for new components.

### Epic 6.5 — a11y & i18n

- `axe-core` runs against the preview after each turn.
- Surface findings as agent events (severity-ranked).
- i18n scaffolding in templates and in the system prompt's conventions.

---

## Cross-cutting concerns (always on)

These are not phases — they apply to every phase, every PR.

### Documentation

- Every public API change updates `docs/architecture.md` or its child docs.
- Every architectural change opens an ADR under `docs/adr/`.
- Every user-facing feature has a one-paragraph entry in `docs/user-guide/` (created in Phase 1).
- Demo gifs live in `docs/media/` and are referenced from the README.

### Testing

- Backend: pytest, ≥80% line coverage on `packages/agent-core` and `apps/api/app/services`.
- Frontend: Karma/Jasmine for components, Playwright for E2E flows.
- One golden-path E2E test per phase, gated in CI.

### Security

- All file writes path-validated against the project workspace root.
- Secrets never logged. CI runs a regex scan against new logs.
- Every dep added requires a one-line justification in the PR description.
- `pip-audit` and `npm audit --audit-level=high` gate CI from Phase 1 onward.

### Performance budgets

- Web: initial JS bundle ≤ 500 KB gzipped (already enforced in `angular.json`).
- API: p95 WebSocket round-trip for a non-LLM event ≤ 50 ms locally.
- Agent loop: cold-start to first streamed token ≤ 1 s for Anthropic.

### Releases

- SemVer. Patch for fixes, minor for additive features, major for breaking changes.
- Tags `vX.Y.Z` cut from `main`. Changelog auto-generated from Conventional Commits.
- Release notes posted to GitHub Releases and pinned in Discussions.

### Community

- Weekly triage: maintainers clear the new-issue queue every Monday.
- Monthly contributor spotlight in Discussions.
- Discord/Matrix once we have ≥50 stars (will be linked from README when live).

---

## How to influence this plan

1. **Open a Discussion** under "Ideas" with your proposal.
2. If it touches architecture, **open an ADR PR** under `docs/adr/`.
3. **Comment on the relevant epic issue** if you want to claim or reshape it.
4. For phase-level changes (re-ordering, splitting, adding), open a PR against this file and tag it `plan-change`.

The plan is the contract between maintainers and contributors. Changing it should be deliberate and visible.
