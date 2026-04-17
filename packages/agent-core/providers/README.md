# LLM provider adapters

Each provider implements the `LLMProvider` interface so the agent loop can stream tokens and execute tool calls without caring which vendor is behind it.

## Status

Phase 0: empty. The interface and the first three implementations (Anthropic, OpenAI, OpenRouter) land in Phase 1.

## Adding a provider (Phase 1+)

1. Create `providers/<name>.py` with a class implementing `LLMProvider`.
2. Register it in `providers/__init__.py`.
3. Add a unit test under `apps/api/tests/providers/`.
4. Document the env vars it expects in `.env.example` and `apps/api/README.md`.

Provider PRs are a great on-ramp: the surface is small, well-isolated, and easy to review.
