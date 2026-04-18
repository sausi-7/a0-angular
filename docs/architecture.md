# Architecture

## One-page view

```
┌────────────────────────┐      ┌─────────────────────────────┐
│  Angular SPA (web UI)  │◄────►│  FastAPI backend            │
│  - Chat panel          │ WS   │  - LLM orchestrator (BYOK)  │
│  - Monaco editor       │ REST │  - Project/file store       │
│  - Preview iframe      │      │  - Agent loop (tool-use)    │
│  - File tree           │      │  - Auth (phase 3+)          │
└────────────┬───────────┘      └──────────────┬──────────────┘
             │                                 │
             │ iframe src=localhost:4201       │ reads/writes
             ▼                                 ▼
      ┌──────────────┐                 ┌────────────────────┐
      │ ng serve     │◄────────────────│ ./workspace/<proj> │
      │ (sidecar)    │   file writes   │ (Angular project)  │
      └──────────────┘                 └────────────────────┘
```

## Components

### `apps/web` — Angular SPA (platform UI)

The thing the user sees. Angular 19, standalone components, Signals. Renders:
- **Chat panel** (left) — messages, streaming tokens
- **Editor / diff view** (center) — Monaco, read-only in Phase 1, editable in Phase 2+
- **File tree** (left sidebar when a project is open)
- **Preview iframe** (right) — points at the sidecar `ng serve` on a per-project port

Talks to `apps/api` over REST (project CRUD, settings) and a single WebSocket per chat session (streaming tokens and file-diff events).

### `apps/api` — FastAPI backend

- Project CRUD (`/projects`, `/projects/{id}`)
- Settings, BYOK keys (stored encrypted)
- Demo bootstrap path (`POST /demo/start`) that seeds `workspace/demo/` from the starter template
- WebSocket endpoint for chat: receives a prompt, kicks off the agent loop, streams back events
- File service: reads/writes under `workspace/<project_id>/`
- Process supervisor for the `ng serve` sidecars (one per active project)

### `packages/agent-core`

Provider-agnostic agent loop. The meat of the LLM behavior.

- `LLMProvider` interface with Anthropic, OpenAI, OpenRouter implementations
- Tool registry: `write_file`, `read_file`, `run_ng_generate`, `edit_file` (Phase 2), `install_package` (Phase 4)
- Prompt templates live in `packages/agent-core/prompts/` as `.md` / `.yaml`
- Event stream: the loop emits typed events (`token`, `tool_call`, `file_changed`, `error`, `done`) that the API forwards to the WebSocket

### `packages/ng-schematics`

Thin wrappers around Angular CLI schematics. Each wrapper is a callable tool the agent can invoke. This keeps "scaffold a component / service / guard" deterministic and cheap instead of asking the LLM to hand-write boilerplate.

### `packages/shared-types`

Pydantic models in the API → TypeScript types in the web app, generated on build. Single source of truth for API contracts.

### `workspace/`

Generated Angular projects live here, one subdirectory per project. Gitignored. The API process is the only writer; the `ng serve` sidecar is read-only against the filesystem.

## Request flow: "build me a todo app"

1. User types prompt in chat. Web opens a WS to `/ws/projects/{id}`.
2. API receives the prompt, loads conversation history and the active system prompt.
3. API calls `agent_core.run(prompt, tools=[...], provider=user_byok_provider)`.
4. Agent loop:
   - Stream tokens → WS → web renders them in the chat panel.
   - When the model emits a tool call (e.g. `write_file`), the loop executes it, pushes a `file_changed` event → WS → web updates the diff view.
   - Repeat until model emits a stop signal.
5. After the first successful `write_file`, API launches an `ng serve` sidecar against `workspace/<id>/` on a per-project port. For the demo path, this is the fixed `workspace/demo/` workspace started by `POST /demo/start`. Web's preview iframe points at it.
6. Hot-reload takes over: subsequent file changes show up in the iframe without platform involvement.

## Data

**Phase 1:** SQLite for metadata (projects, messages, settings). Files on disk.
**Phase 3+:** Postgres via Alembic. SQLAlchemy 2.0 async is used from Phase 1 so the swap is a config change.

## Plugin seams

Three extension points exist from day one so contributors can add alternatives without touching core code:

1. **`LLMProvider`** — add a new provider by implementing the interface and registering it in the provider registry.
2. **`SandboxBackend`** — Phase 1 has only `LocalSandbox`. Phase 5 adds Docker and E2B implementations.
3. **Tool registry** — new agent tools register themselves via decorator; no core changes required.

## Security notes

- User-supplied API keys are encrypted at rest using `A0_SECRET_KEY` (per-deployment).
- All file writes from tools are path-validated against the project's workspace root — no traversal.
- `ng serve` sidecars run as a less-privileged user in Phase 5 Docker mode. In Phase 1 local-only mode, the operator trusts generated code by running it on their own machine.
- See [SECURITY.md](../SECURITY.md) for reporting.

## Open questions (tracked as ADRs)

- Full sandbox strategy beyond Phase 1 — see [ADR-0004 (TBD)](adr/).
- How to represent chat history compactly for long-running projects (context compression). Phase 2.
- Multi-tenancy model once hosted by third parties — Phase 3.
