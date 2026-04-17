# ADR-0001: Stack — Angular frontend, FastAPI backend

- Status: Accepted
- Date: 2026-04-17

## Context

We are building an open-source vibe-coding platform specialized for Angular. The platform UI and the generated apps are both in scope; they are separate concerns but the UI choice is also a dogfooding signal.

We need a backend with good streaming (WebSockets), strong typing, and a healthy LLM ecosystem. We need a frontend with a real code editor, iframe sandboxing for preview, and fast streaming UI.

## Decision

- **Frontend:** Angular 19, standalone components, Signals, Tailwind, Monaco.
- **Backend:** FastAPI + Pydantic v2, SQLAlchemy 2.0 async, `anthropic` / `openai` / `litellm` SDKs.
- **Monorepo** under `apps/` and `packages/`.
- **Package managers:** `npm` for web, `uv` for Python. (pnpm is faster but adds an install step; we optimize for contributor onboarding.)

## Consequences

Positive:
- We dogfood Angular — contributors who want to build the platform must know Angular, which seeds the quality of Angular-specific guardrails in generated output.
- FastAPI's streaming, OpenAPI generation, and Pydantic story cover most backend needs out-of-box.
- Both ecosystems have first-class typing; we avoid two dynamic-typing tax lanes.

Negative:
- Smaller Angular community than React for platform UI contributions. Offset by lowering the bar (prompt templates, schematic tools, provider adapters are all writable without Angular expertise).
- Angular's build tooling is heavier than Vite-only React setups. Acceptable — we only ship one SPA.

Follow-ups:
- Pin Angular major versions in CI to catch breakage from new releases.

## Alternatives considered

- **React + Next.js frontend.** Larger contributor pool, but dogfooding the target stack is the stronger signal and encodes empathy for Angular users.
- **Express / Node backend.** One-language stack appeals, but the Python LLM ecosystem (SDKs, evals, agent libs) is further along.
- **Go backend.** Faster, but thinner LLM ecosystem and slower prototyping.
