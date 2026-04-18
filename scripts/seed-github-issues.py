#!/usr/bin/env python3
"""
Seed GitHub labels and Phase 1 issues for A0 for Angular.

Prereqs:
  - gh CLI installed and authenticated (`gh auth status`)
  - Run from anywhere — paths resolve relative to this file.

Idempotent for labels (uses --force). NOT idempotent for issues —
re-running creates duplicates. Run once.

Usage:
  python3 scripts/seed-github-issues.py                   # slice + Phase 1 + tracking issues
  python3 scripts/seed-github-issues.py --slice-only      # just Phase 1.0 demo-slice issues
  python3 scripts/seed-github-issues.py --dry-run         # print, don't create
  python3 scripts/seed-github-issues.py --repo foo/bar
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass

DEFAULT_REPO = "sausi-7/a0-angular"


# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------

LABELS: list[tuple[str, str, str]] = [
    ("D1", "0e8a16", "Good first issue — self-contained and well-specified"),
    ("D2", "fbca04", "Intermediate — touches one subsystem"),
    ("D3", "d93f0b", "Advanced — design discussion expected before code"),
    ("good first issue", "7057ff", "Curated on-ramp for new contributors"),
    ("phase-1.0", "0366d6", "Phase 1.0 — demo-ready vertical slice (launch gif)"),
    ("phase-1", "1d76db", "Phase 1 — MVP: prompt → working app"),
    ("phase-2", "1d76db", "Phase 2 — iterative editing"),
    ("slice:demo", "bfd4f2", "Part of the launch-day demo-gif slice"),
    ("epic:agent-core", "c5def5", "Lives under packages/agent-core"),
    ("epic:api", "c5def5", "Lives under apps/api"),
    ("epic:web", "c5def5", "Lives under apps/web"),
    ("epic:sidecar", "c5def5", "ng serve process supervision"),
    ("epic:e2e", "c5def5", "End-to-end testing infra"),
    ("epic:storage", "c5def5", "Persistence and BYOK"),
    ("tracking", "5319e7", "Tracking / meta issue"),
    ("plan-change", "5319e7", "Proposes a change to PLAN.md"),
]


# ---------------------------------------------------------------------------
# Issues
# ---------------------------------------------------------------------------

@dataclass
class Issue:
    title: str
    labels: list[str]
    body: str


SLICE_TRACKING = Issue(
    title="Phase 1.0 tracking — demo-ready vertical slice",
    labels=["tracking", "phase-1.0", "slice:demo"],
    body="""\
This is the meta-tracking issue for **Phase 1.0 — Demo-ready vertical slice**.

Read the [Phase 1.0 section in PLAN.md](../blob/main/PLAN.md#phase-10--demo-ready-vertical-slice) for the full rationale and cuts.

## Why this exists

Posting about the project on r/Angular before there is a working demo will land with a thud. Phase 1.0 is the smallest cut that produces a 30-second gif of `prompt → streamed file changes → working preview`. Everything not visible in the gif is deferred.

## Cuts

- One provider (Anthropic), key from env, no BYOK UI
- One project, fixed id `demo`, fixed sidecar port `4300`
- Two tools only: `write_file`, `read_file`
- In-memory project state, no DB
- Pre-seeded Angular starter so `ng serve` boots in seconds

## Suggested order for a solo contributor

1. `1.0.1` → `1.0.2` → `1.0.3` → `1.0.4` → `1.0.5`  (backend agent works against `workspace/demo/`)
2. `1.0.6` → `1.0.7` → `1.0.8`  (API + sidecar)
3. `1.0.9` → `1.0.10` → `1.0.11`  (web)
4. `1.0.12`  (template + gif — the deliverable)

## Exit criteria

- `make dev` + `ANTHROPIC_API_KEY` is the entire setup.
- Configured prompt produces a runnable todo app at the iframe URL.
- `docs/media/demo.gif` committed and embedded in the README.
- CI green.

After this ships: post to r/Angular with the gif. Then continue full Phase 1 in parallel — slice code is the foundation, not throwaway.
""",
)


TRACKING = Issue(
    title="Phase 1 tracking — pick an epic",
    labels=["tracking", "phase-1"],
    body="""\
This is the meta-tracking issue for **Phase 1 — MVP: Prompt → Working Angular App**.

Read [PLAN.md](../blob/main/PLAN.md) for the full plan. Phase 1 is split into 5 epics that can run in parallel:

- **Epic 1.1 — Agent core** (`packages/agent-core`): the LLM loop and tools
- **Epic 1.2 — API surface** (`apps/api`): REST + WebSocket endpoints
- **Epic 1.3 — Web UI** (`apps/web`): chat, file diff, preview iframe
- **Epic 1.4 — Sidecar `ng serve` manager**: process supervision
- **Epic 1.5 — End-to-end testing**: Playwright + smoke flows

## How to claim work

1. Browse open Phase 1 issues filtered by `D1` (good first issue), `D2` (intermediate), or `D3` (advanced).
2. Comment "I'd like to take this" on the issue.
3. A maintainer assigns within 48h.

## Phase 1 exit criteria

1. User submits a prompt and watches files stream into `workspace/<project>/`.
2. A sidecar `ng serve` boots the project and renders it in the preview iframe.
3. Loop works with at least one BYOK provider (Anthropic).
4. Headless E2E test asserts the preview returns 200.
5. Architecture docs updated; demo gif in README.

We move to Phase 2 only after all five exit criteria are met.
""",
)


SLICE_ISSUES: list[Issue] = [
    Issue(
        "slice 1.0.1: AnthropicProvider — minimal streaming + tool use",
        ["phase-1.0", "slice:demo", "epic:agent-core", "D2"],
        """\
**Phase 1.0 demo slice · Difficulty:** D2

## Scope
The smallest workable `LLMProvider` ABC and a single `AnthropicProvider` implementation. No factory, no provider switching. Key read from `ANTHROPIC_API_KEY` env var (BYOK UI is deferred to full Phase 1).

## Acceptance criteria
- [ ] `LLMProvider.stream(messages, tools) -> AsyncIterator[Event]` defined.
- [ ] Events: `token`, `tool_call`, `tool_result`, `done`, `error`.
- [ ] `AnthropicProvider` streams tokens and surfaces tool-use blocks.
- [ ] Smoke test (manual is fine for the slice; recorded fixture preferred).

Carries forward into full Phase 1 issue 1.1.2 with no rewrite.
""",
    ),
    Issue(
        "slice 1.0.2: write_file tool with workspace-root path validation",
        ["phase-1.0", "slice:demo", "epic:agent-core", "D2"],
        """\
**Phase 1.0 demo slice · Difficulty:** D2

## Scope
`write_file(path, content)` tool. Path resolved against the demo workspace root; reject `..`, absolute paths, symlink escape.

## Acceptance criteria
- [ ] Creates parent dirs as needed.
- [ ] Emits a `file_changed` event after a successful write.
- [ ] Unit tests for traversal / absolute / symlink-escape rejection.

Same code as full Phase 1 issue 1.1.6.
""",
    ),
    Issue(
        "slice 1.0.3: read_file tool with 256 KB cap",
        ["phase-1.0", "slice:demo", "epic:agent-core", "D1", "good first issue"],
        """\
**Phase 1.0 demo slice · Difficulty:** D1 (good first issue)

## Scope
`read_file(path)`. 256 KB cap. UTF-8 decode; clear error on binary.

## Acceptance criteria
- [ ] Returns content under cap, errors clearly over.
- [ ] Same path validation as `write_file`.
- [ ] Tests for cap, binary, missing.
""",
    ),
    Issue(
        "slice 1.0.4: agent loop runner — provider + tool dispatch + event emit",
        ["phase-1.0", "slice:demo", "epic:agent-core", "D2"],
        """\
**Phase 1.0 demo slice · Difficulty:** D2

## Scope
The minimum loop: take a system prompt + user prompt + provider + tool registry; stream events; dispatch tool calls; feed results back; terminate on `done`.

No token-budget trimming, no conversation persistence, no multi-turn — that's deferred.

## Acceptance criteria
- [ ] Async function returning an `AsyncIterator[Event]`.
- [ ] Tool-call → tool-result round-trip works against `write_file` and `read_file`.
- [ ] Loop terminates cleanly on `done` or `error`.
- [ ] Smoke test against a `FakeProvider` that scripts a `write_file` call.
""",
    ),
    Issue(
        "slice 1.0.5: system prompt for the todo-app happy path",
        ["phase-1.0", "slice:demo", "epic:agent-core", "D1", "good first issue"],
        """\
**Phase 1.0 demo slice · Difficulty:** D1 (good first issue)

## Scope
`packages/agent-core/prompts/system_demo.md`. Tight prompt that, given the user prompt "Build me a todo app with localStorage" and access to a pre-seeded Angular starter, produces a working app.

## Acceptance criteria
- [ ] Markdown file with: project layout assumptions, tools available, Angular 19 conventions (standalone, Signals, new control flow).
- [ ] Manually verified: prompt + Anthropic + the two tools produces a runnable todo app on at least 3 of 5 attempts.
- [ ] Failure modes documented in the file's footer.
""",
    ),
    Issue(
        "slice 1.0.6: POST /demo/start — seed workspace from starter template",
        ["phase-1.0", "slice:demo", "epic:api", "D1", "good first issue"],
        """\
**Phase 1.0 demo slice · Difficulty:** D1 (good first issue)

## Scope
`POST /demo/start` copies `packages/templates/demo-starter/` into `workspace/demo/`, returns `{ready: true, preview_port: 4300}`. Idempotent — re-running wipes and re-seeds.

## Acceptance criteria
- [ ] Endpoint exists and returns 200.
- [ ] Workspace contents match the starter after the call.
- [ ] Integration test against a temp workspace dir.
""",
    ),
    Issue(
        "slice 1.0.7: WS /ws/demo — stream agent events for a single prompt",
        ["phase-1.0", "slice:demo", "epic:api", "D2"],
        """\
**Phase 1.0 demo slice · Difficulty:** D2

## Scope
WebSocket endpoint. One inbound message: `{prompt: string}`. Many outbound: every event from the agent loop. Closes on `done` or `error`.

No reconnect/replay logic for the slice — refresh-on-disconnect is acceptable.

## Acceptance criteria
- [ ] Endpoint at `/ws/demo`.
- [ ] Forwards every loop event verbatim.
- [ ] Integration test using `FakeProvider`.
""",
    ),
    Issue(
        "slice 1.0.8: sidecar manager (single instance) — ng serve --port 4300",
        ["phase-1.0", "slice:demo", "epic:sidecar", "D2"],
        """\
**Phase 1.0 demo slice · Difficulty:** D2

## Scope
Spawn one `ng serve --port 4300` against `workspace/demo/` when the API starts (or on first `/demo/start` call). Kill on API shutdown via `atexit`.

No port pool, no multi-project — that's full Phase 1.

## Acceptance criteria
- [ ] No orphan `ng serve` after `Ctrl+C` on the API.
- [ ] Health probe at `localhost:4300/` returns 200 once compiled.
- [ ] Documented in `apps/api/README.md`.
""",
    ),
    Issue(
        "slice 1.0.9: web shell — two-pane layout (prompt + log | preview)",
        ["phase-1.0", "slice:demo", "epic:web", "D1", "good first issue"],
        """\
**Phase 1.0 demo slice · Difficulty:** D1 (good first issue)

## Scope
Standalone Angular component. Left: textarea + submit + scrolling event log. Right: preview iframe placeholder. Tailwind. No splitter, no resizing.

## Acceptance criteria
- [ ] Renders at ≥1280px.
- [ ] Submit button disables while a stream is in flight.
- [ ] Component spec.
""",
    ),
    Issue(
        "slice 1.0.10: WebSocket client service for /ws/demo",
        ["phase-1.0", "slice:demo", "epic:web", "D2"],
        """\
**Phase 1.0 demo slice · Difficulty:** D2

## Scope
Injectable Angular service. Connects to `/ws/demo`, sends `{prompt}`, parses incoming events, pushes them into a `WritableSignal<Event[]>`.

No reconnect logic — refresh on disconnect is fine for the slice.

## Acceptance criteria
- [ ] Typed events match the agent-core event union.
- [ ] Service spec covers connect / send / receive / close.
""",
    ),
    Issue(
        "slice 1.0.11: preview iframe — poll port, then load",
        ["phase-1.0", "slice:demo", "epic:web", "D1", "good first issue"],
        """\
**Phase 1.0 demo slice · Difficulty:** D1 (good first issue)

## Scope
Iframe component pointing at `http://localhost:4300/`. Until the port returns 200, show a "preview booting…" state. After the first successful response, load the iframe and reload it on each `done` event.

## Acceptance criteria
- [ ] Iframe `sandbox` attributes documented.
- [ ] Booting → ready → reload-on-done states observable in DevTools.
- [ ] Component spec.
""",
    ),
    Issue(
        "slice 1.0.12: starter template + record demo.gif (the deliverable)",
        ["phase-1.0", "slice:demo", "D2"],
        """\
**Phase 1.0 demo slice · Difficulty:** D2

## Scope
This is the launch deliverable. Two parts:

1. **Starter template** at `packages/templates/demo-starter/` — a minimal Angular 19 app with one empty component the agent will populate. Pre-installed `node_modules` are NOT committed; first `/demo/start` runs `npm ci` once and caches.
2. **Demo gif** at `docs/media/demo.gif` — 30-second screen capture of: open app → type "Build me a todo app with localStorage" → file events stream → preview iframe shows working todo app → user adds a todo.

## Acceptance criteria
- [ ] Starter boots with `ng serve --port 4300` in under 10s on a warm cache.
- [ ] `docs/media/demo.gif` ≤ 5 MB, embedded in `README.md`.
- [ ] README's "Status" section updated from Phase 0 to "Phase 1.0 — demo works."

After this ships, the launch post on r/Angular is unblocked.
""",
    ),
]


ISSUES: list[Issue] = [
    # -----------------------------------------------------------------------
    # Epic 1.1 — Agent core
    # -----------------------------------------------------------------------
    Issue(
        "agent-core: define LLMProvider interface and event types",
        ["phase-1", "epic:agent-core", "D2"],
        """\
**Epic:** 1.1 Agent core · **Difficulty:** D2

## Scope
Define the `LLMProvider` Pydantic interface and the typed event stream the loop emits.

## Events to support
- `token` — incremental text from the model
- `tool_call` — model wants to invoke a tool
- `tool_result` — result of executing a tool call
- `file_changed` — workspace file added/modified/deleted
- `error` — recoverable or fatal error
- `done` — loop terminated

## Acceptance criteria
- [ ] Pydantic models for each event type, with a discriminated union.
- [ ] `LLMProvider` ABC with `stream(messages, tools) -> AsyncIterator[Event]`.
- [ ] Documented in `packages/agent-core/README.md`.
- [ ] `make lint test` passes.
""",
    ),
    Issue(
        "agent-core: implement AnthropicProvider with streaming + tool use",
        ["phase-1", "epic:agent-core", "D2"],
        """\
**Epic:** 1.1 Agent core · **Difficulty:** D2

## Scope
Implement `AnthropicProvider` against the official `anthropic` SDK. Must stream tokens and surface tool-use blocks as `tool_call` events.

## Acceptance criteria
- [ ] Streams `token` events as the model writes.
- [ ] Emits `tool_call` events when the model issues a tool use.
- [ ] Honors BYOK: API key passed in via constructor, never read from env in the provider class itself.
- [ ] Unit test against a recorded fixture (no live API calls in CI).
- [ ] Cite [docs/adr/0002-byok.md](../blob/main/docs/adr/0002-byok.md) for key handling.
""",
    ),
    Issue(
        "agent-core: implement OpenAIProvider",
        ["phase-1", "epic:agent-core", "D2"],
        """\
**Epic:** 1.1 Agent core · **Difficulty:** D2

Mirror the AnthropicProvider implementation against the OpenAI SDK.

## Acceptance criteria
- [ ] Streams `token` and `tool_call` events.
- [ ] Same constructor surface as AnthropicProvider (BYOK).
- [ ] Unit test with recorded fixture.
""",
    ),
    Issue(
        "agent-core: implement OpenRouterProvider",
        ["phase-1", "epic:agent-core", "D2"],
        """\
**Epic:** 1.1 Agent core · **Difficulty:** D2

OpenRouter exposes an OpenAI-compatible API. Subclass or compose with the OpenAI provider; switch base URL and validate model strings.

## Acceptance criteria
- [ ] Works with at least 2 OpenRouter-hosted models (e.g. one Anthropic, one Mistral).
- [ ] Unit test with recorded fixture.
""",
    ),
    Issue(
        "agent-core: tool registry with @tool decorator and Pydantic arg schemas",
        ["phase-1", "epic:agent-core", "D3"],
        """\
**Epic:** 1.1 Agent core · **Difficulty:** D3

Build the registry that lets tools self-register and the loop introspect Pydantic schemas to produce provider-specific tool definitions (Anthropic / OpenAI / OpenRouter formats differ).

## Acceptance criteria
- [ ] `@tool` decorator wraps a function with a Pydantic args model.
- [ ] Registry exposes `as_anthropic_tools()`, `as_openai_tools()` etc.
- [ ] Adding a new tool requires only the decorator + import — no central list edits.
- [ ] Unit tests cover schema generation for both provider formats.
""",
    ),
    Issue(
        "agent-core: tool — write_file with workspace-root path validation",
        ["phase-1", "epic:agent-core", "D2"],
        """\
**Epic:** 1.1 Agent core · **Difficulty:** D2

Implement the `write_file(path, content)` tool. Path must be inside the project workspace root; reject `..`, absolute paths, and symlinks that escape the root.

## Acceptance criteria
- [ ] Resolves path against workspace root; rejects traversal.
- [ ] Creates parent directories as needed.
- [ ] Emits a `file_changed` event after a successful write.
- [ ] Unit tests for the security cases (traversal, absolute path, symlink escape).
""",
    ),
    Issue(
        "agent-core: tool — read_file with size cap",
        ["phase-1", "epic:agent-core", "D1", "good first issue"],
        """\
**Epic:** 1.1 Agent core · **Difficulty:** D1 (good first issue)

Implement `read_file(path)`. 256 KB cap. UTF-8 decode; clear error on binary.

## Acceptance criteria
- [ ] Returns file content under the cap; errors clearly over.
- [ ] Same path-validation as `write_file`.
- [ ] Unit tests for cap, binary file, missing file.
""",
    ),
    Issue(
        "agent-core: tool — run_ng_generate (delegates to ng-schematics)",
        ["phase-1", "epic:agent-core", "D2"],
        """\
**Epic:** 1.1 Agent core · **Difficulty:** D2

Wrap `ng generate <schematic> <name> [--options]` as a tool. Implementation lives in `packages/ng-schematics`; the agent-core import surfaces it as a registered tool.

## Acceptance criteria
- [ ] Tool runs against the project workspace dir as cwd.
- [ ] Returns the list of files created/modified.
- [ ] Error output is captured into the `tool_result`.
- [ ] Unit test against a fixture project.
""",
    ),
    Issue(
        "agent-core: conversation state with token-budget trimming",
        ["phase-1", "epic:agent-core", "D2"],
        """\
**Epic:** 1.1 Agent core · **Difficulty:** D2

Hold messages + tool results between turns; trim oldest non-system messages when over the per-provider token budget.

## Acceptance criteria
- [ ] `Conversation` class with `add()` and `for_provider()`.
- [ ] Trim strategy is documented and unit-tested.
- [ ] System messages always retained.
""",
    ),
    Issue(
        "agent-core: write Phase 1 system prompt encoding Angular 19 conventions",
        ["phase-1", "epic:agent-core", "D1", "good first issue"],
        """\
**Epic:** 1.1 Agent core · **Difficulty:** D1 (good first issue)

Write `packages/agent-core/prompts/system_angular.md`. Cover: standalone components, Signals, new control flow (`@if` / `@for` / `@switch`), functional guards, DI patterns, no `NgModule`s in new code.

## Acceptance criteria
- [ ] Markdown file under `packages/agent-core/prompts/`.
- [ ] At least one positive and one negative example per convention.
- [ ] Reviewed by at least one Angular practitioner.
""",
    ),
    Issue(
        "agent-core: unit tests using FakeProvider for deterministic loop testing",
        ["phase-1", "epic:agent-core", "D2"],
        """\
**Epic:** 1.1 Agent core · **Difficulty:** D2

Implement a `FakeProvider` that returns a scripted sequence of tokens and tool calls. Use it to test the loop end-to-end without API calls.

## Acceptance criteria
- [ ] `FakeProvider` configurable per test.
- [ ] Loop tests cover: plain response, single tool call, multi-tool sequence, error path.
- [ ] Coverage on the loop module ≥ 80%.
""",
    ),
    # -----------------------------------------------------------------------
    # Epic 1.2 — API surface
    # -----------------------------------------------------------------------
    Issue(
        "api: POST /projects creates project, allocates workspace + sidecar port",
        ["phase-1", "epic:api", "D1", "good first issue"],
        """\
**Epic:** 1.2 API surface · **Difficulty:** D1 (good first issue)

## Acceptance criteria
- [ ] `POST /projects {name}` returns `{id, workspace_path, preview_port}`.
- [ ] Workspace dir created under `workspace/<id>/`.
- [ ] Port allocated from a configurable pool (default 4201–4299).
- [ ] Unit + integration test.
""",
    ),
    Issue(
        "api: GET /projects and GET /projects/{id}",
        ["phase-1", "epic:api", "D1", "good first issue"],
        """\
**Epic:** 1.2 API surface · **Difficulty:** D1 (good first issue)

## Acceptance criteria
- [ ] `GET /projects` lists all projects (no auth in Phase 1).
- [ ] `GET /projects/{id}` returns detail with file count and last-message timestamp.
- [ ] 404 on missing.
- [ ] Tests.
""",
    ),
    Issue(
        "api: WebSocket /ws/projects/{id} streams agent events",
        ["phase-1", "epic:api", "D3"],
        """\
**Epic:** 1.2 API surface · **Difficulty:** D3

Bridge the agent loop to the client. Receives a single `{prompt}` message, forwards every agent event, closes on `done` or `error`.

## Acceptance criteria
- [ ] One inbound message per session; many outbound events.
- [ ] Backpressure-aware (don't drop tokens under slow clients).
- [ ] Survives client reconnect within 30s by replaying buffered events.
- [ ] Integration test with FakeProvider.
""",
    ),
    Issue(
        "api: read-only file endpoints for Monaco editor",
        ["phase-1", "epic:api", "D2"],
        """\
**Epic:** 1.2 API surface · **Difficulty:** D2

`GET /projects/{id}/files` returns the file tree. `GET /projects/{id}/files/{path}` returns content.

## Acceptance criteria
- [ ] Tree endpoint streams large trees efficiently.
- [ ] Content endpoint enforces path validation and the 256 KB cap.
- [ ] Tests for traversal attempts.
""",
    ),
    Issue(
        "storage: SQLAlchemy 2.0 async models — Project, Message, Setting",
        ["phase-1", "epic:storage", "D2"],
        """\
**Epic:** 1.2 API surface (storage) · **Difficulty:** D2

SQLite via `aiosqlite`. Models with timestamps, soft-delete on Project.

## Acceptance criteria
- [ ] Async session factory in `apps/api/app/db.py`.
- [ ] Models with relationships.
- [ ] Repository classes (`ProjectRepo`, `MessageRepo`, `SettingRepo`).
- [ ] Tests using a temp SQLite file.
""",
    ),
    Issue(
        "storage: BYOK settings endpoints with encrypted key column",
        ["phase-1", "epic:storage", "D2"],
        """\
**Epic:** 1.2 API surface (storage) · **Difficulty:** D2

`POST /settings/keys`, `GET /settings/keys`, `DELETE /settings/keys/{provider}`. Keys encrypted at rest with `cryptography.Fernet` keyed off `A0_SECRET_KEY`.

## Acceptance criteria
- [ ] Keys never returned in API responses (only `{provider, last4}`).
- [ ] Keys never written to logs (CI regex check).
- [ ] Tests for encrypt/decrypt round-trip.
""",
    ),
    Issue(
        "api: structured JSON logging with secret-redaction",
        ["phase-1", "epic:api", "D1", "good first issue"],
        """\
**Epic:** 1.2 API surface · **Difficulty:** D1 (good first issue)

Wire `structlog` for JSON logs. Add a processor that redacts known-secret keys (`api_key`, `authorization`, etc.).

## Acceptance criteria
- [ ] Logs are valid JSON.
- [ ] Redaction processor unit-tested.
- [ ] CI grep test fails the build if a literal secret pattern shows up in the output of the test suite.
""",
    ),
    Issue(
        "api: OpenAPI export script feeding shared-types codegen",
        ["phase-1", "epic:api", "D2"],
        """\
**Epic:** 1.2 API surface · **Difficulty:** D2

`python -m app.export_openapi > openapi.json`. Wire `openapi-typescript` in `packages/shared-types` to consume it. Add a CI step.

## Acceptance criteria
- [ ] Script generates a valid OpenAPI spec.
- [ ] `packages/shared-types/index.ts` regenerated and committed.
- [ ] CI fails on drift between models and committed types.
""",
    ),
    # -----------------------------------------------------------------------
    # Epic 1.3 — Web UI
    # -----------------------------------------------------------------------
    Issue(
        "web: three-pane layout — chat, preview, file diff overlay",
        ["phase-1", "epic:web", "D2"],
        """\
**Epic:** 1.3 Web UI · **Difficulty:** D2

Standalone Angular component. Tailwind utilities. Resizable splitter between chat and preview.

## Acceptance criteria
- [ ] Layout renders at all viewport widths ≥ 1024px.
- [ ] Splitter position persists in localStorage.
- [ ] Storybook-style example screenshot in PR.
""",
    ),
    Issue(
        "web: chat input + message list with streaming token rendering",
        ["phase-1", "epic:web", "D2"],
        """\
**Epic:** 1.3 Web UI · **Difficulty:** D2

Render a conversation. Append `token` events to the active assistant message without re-rendering the whole list.

## Acceptance criteria
- [ ] Uses Signals + `@for` with `track`.
- [ ] No layout thrash during a 5000-token stream (verify in DevTools).
- [ ] Markdown rendering for assistant messages.
- [ ] Component spec.
""",
    ),
    Issue(
        "web: WebSocket service subscribing to /ws/projects/{id}",
        ["phase-1", "epic:web", "D2"],
        """\
**Epic:** 1.3 Web UI · **Difficulty:** D2

Injectable Angular service. Reconnect with exponential backoff. Exposes typed event Observables (or Signals).

## Acceptance criteria
- [ ] Reconnect on close ≠ 1000 with backoff.
- [ ] Events are typed via `@a0-angular/shared-types`.
- [ ] Service spec covers reconnect.
""",
    ),
    Issue(
        "web: file diff overlay animating each file_changed event",
        ["phase-1", "epic:web", "D2"],
        """\
**Epic:** 1.3 Web UI · **Difficulty:** D2

When a `file_changed` event arrives, slide in a card showing path + a brief diff. Auto-dismiss after N seconds; stack multiple.

## Acceptance criteria
- [ ] Animation runs ≤ 16ms per frame on a mid-tier laptop.
- [ ] Stacking caps at 5; older cards collapse.
- [ ] Component spec.
""",
    ),
    Issue(
        "web: preview iframe pointing at sidecar ng serve port",
        ["phase-1", "epic:web", "D1", "good first issue"],
        """\
**Epic:** 1.3 Web UI · **Difficulty:** D1 (good first issue)

Iframe with `sandbox` attributes. Reads port from the project detail. Shows a loading state until the sidecar responds 200.

## Acceptance criteria
- [ ] Iframe sandbox attributes documented.
- [ ] Loading / error / ready states.
- [ ] Component spec.
""",
    ),
    Issue(
        "web: Monaco editor (read-only) with lazy bundle",
        ["phase-1", "epic:web", "D2"],
        """\
**Epic:** 1.3 Web UI · **Difficulty:** D2

Lazy-load Monaco via dynamic import so initial bundle stays under 500 KB gzip.

## Acceptance criteria
- [ ] Monaco loads only when the user opens a file.
- [ ] Build still respects the 500 KB initial budget in `angular.json`.
- [ ] TypeScript and HTML language modes.
""",
    ),
    Issue(
        "web: BYOK settings screen — provider, model, masked key",
        ["phase-1", "epic:web", "D2"],
        """\
**Epic:** 1.3 Web UI · **Difficulty:** D2

Form to configure each provider. Key is masked (`••••last4`) after save; never logged.

## Acceptance criteria
- [ ] One row per provider (Anthropic / OpenAI / OpenRouter).
- [ ] Validation: non-empty key, sensible model string.
- [ ] No `console.log` of key values (CI grep check).
""",
    ),
    Issue(
        "web: project picker / new-project flow",
        ["phase-1", "epic:web", "D1", "good first issue"],
        """\
**Epic:** 1.3 Web UI · **Difficulty:** D1 (good first issue)

Landing screen lists projects + "New project" CTA. Persists last-opened project ID in localStorage.

## Acceptance criteria
- [ ] List, create, open flows.
- [ ] Last-opened restored on reload.
- [ ] Component spec.
""",
    ),
    # -----------------------------------------------------------------------
    # Epic 1.4 — Sidecar ng serve manager
    # -----------------------------------------------------------------------
    Issue(
        "sidecar: process supervisor — spawn / kill / restart ng serve per project",
        ["phase-1", "epic:sidecar", "D3"],
        """\
**Epic:** 1.4 Sidecar manager · **Difficulty:** D3

Allocate a port from a pool, spawn `ng serve --port <p>` against the workspace, kill on project delete, restart on demand.

## Acceptance criteria
- [ ] No orphan processes after API restart (PID file or supervisor).
- [ ] Port pool exhaustion returns a clear error.
- [ ] Integration test that spawns and kills a sidecar against a fixture project.
""",
    ),
    Issue(
        "sidecar: health probe before unblocking the iframe",
        ["phase-1", "epic:sidecar", "D2"],
        """\
**Epic:** 1.4 Sidecar manager · **Difficulty:** D2

`GET http://localhost:<port>/` polled until 200; surfaces `preview_status` events to the WebSocket.

## Acceptance criteria
- [ ] Polling interval and timeout configurable.
- [ ] Emits `preview_booting`, `preview_ready`, `preview_failed` events.
- [ ] Test against a fixture HTTP server.
""",
    ),
    Issue(
        "sidecar: capture stderr and forward compile errors as agent events",
        ["phase-1", "epic:sidecar", "D2"],
        """\
**Epic:** 1.4 Sidecar manager · **Difficulty:** D2

Foundation for Phase 2's error-feedback loop. Tail `ng serve` stderr; parse compile errors; emit `build_error` events.

## Acceptance criteria
- [ ] Parser handles tsc and Angular template errors.
- [ ] Events include file path, line, message.
- [ ] Unit tests with sample stderr fixtures.
""",
    ),
    # -----------------------------------------------------------------------
    # Epic 1.5 — End-to-end testing
    # -----------------------------------------------------------------------
    Issue(
        "e2e: Playwright setup in CI with headless Chrome",
        ["phase-1", "epic:e2e", "D2"],
        """\
**Epic:** 1.5 E2E testing · **Difficulty:** D2

Add Playwright as a dev dep. CI job installs browsers and runs against a freshly-built stack.

## Acceptance criteria
- [ ] `npm run e2e` works locally.
- [ ] CI job runs on PRs touching `apps/web` or `apps/api`.
- [ ] Failure traces uploaded as artifacts.
""",
    ),
    Issue(
        "e2e: golden-path test using FakeProvider — generate hello-world component",
        ["phase-1", "epic:e2e", "D2"],
        """\
**Epic:** 1.5 E2E testing · **Difficulty:** D2

End-to-end: open the app, submit a prompt, watch a file_changed event, assert the preview iframe responds 200.

## Acceptance criteria
- [ ] Test runs in <60s in CI.
- [ ] Uses FakeProvider — no real LLM call.
- [ ] Asserts the generated file exists and the preview returns 200.
""",
    ),
    Issue(
        "e2e: nightly smoke test against real Anthropic with cassette replay",
        ["phase-1", "epic:e2e", "D3"],
        """\
**Epic:** 1.5 E2E testing · **Difficulty:** D3

Use `vcr.py`-style cassettes. Real call records once; CI replays. Nightly job re-records to catch drift.

## Acceptance criteria
- [ ] Cassette format documented.
- [ ] Nightly cron job re-records and opens an issue on diff.
- [ ] Real-call test gated on a CI secret; skipped if not set.
""",
    ),
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run(cmd: list[str], dry: bool) -> None:
    if dry:
        print("  $", " ".join(cmd))
        return
    subprocess.run(cmd, check=True, capture_output=True)


def ensure_gh() -> None:
    if shutil.which("gh") is None:
        sys.exit("gh CLI not found. Install with: brew install gh")
    result = subprocess.run(["gh", "auth", "status"], capture_output=True)
    if result.returncode != 0:
        sys.exit("gh not authenticated. Run: gh auth login")


def create_labels(repo: str, dry: bool) -> None:
    print("==> Creating labels")
    for name, color, desc in LABELS:
        print(f"    - {name}")
        run(
            [
                "gh", "label", "create", name,
                "--color", color,
                "--description", desc,
                "--force",
                "--repo", repo,
            ],
            dry,
        )


def create_issue(repo: str, issue: Issue, dry: bool) -> None:
    print(f"==> Issue: {issue.title}")
    run(
        [
            "gh", "issue", "create",
            "--repo", repo,
            "--title", issue.title,
            "--label", ",".join(issue.labels),
            "--body", issue.body,
        ],
        dry,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=DEFAULT_REPO, help=f"GitHub repo (default: {DEFAULT_REPO})")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing")
    parser.add_argument("--labels-only", action="store_true", help="Only create labels, skip issues")
    parser.add_argument("--slice-only", action="store_true", help="Only seed Phase 1.0 demo-slice issues + tracker")
    args = parser.parse_args()

    if not args.dry_run:
        ensure_gh()

    create_labels(args.repo, args.dry_run)

    if args.labels_only:
        return

    print("\n==> Creating Phase 1.0 slice tracking issue")
    create_issue(args.repo, SLICE_TRACKING, args.dry_run)

    print(f"\n==> Creating {len(SLICE_ISSUES)} Phase 1.0 slice issues")
    for issue in SLICE_ISSUES:
        create_issue(args.repo, issue, args.dry_run)

    if args.slice_only:
        print(f"\n==> Done (slice only). View at https://github.com/{args.repo}/issues")
        return

    print("\n==> Creating Phase 1 tracking issue")
    create_issue(args.repo, TRACKING, args.dry_run)

    print(f"\n==> Creating {len(ISSUES)} Phase 1 issues")
    for issue in ISSUES:
        create_issue(args.repo, issue, args.dry_run)

    print(f"\n==> Done. View at https://github.com/{args.repo}/issues")


if __name__ == "__main__":
    main()
