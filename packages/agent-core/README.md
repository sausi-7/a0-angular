# packages/agent-core

Provider-agnostic LLM agent loop used by `apps/api`.

## Responsibilities

- Define the `LLMProvider` interface and implementations (Anthropic, OpenAI, OpenRouter, Ollama).
- Define the tool registry: `write_file`, `read_file`, `run_ng_generate`, `edit_file`, etc.
- Run the loop: stream model tokens, execute tool calls, emit typed events.
- Host prompt templates as data in `prompts/` so non-engineers can contribute.

## Status

Phase 0: placeholder. Implementation lands in Phase 1.

## Contributing

Great on-ramps for new contributors once this lands:
- Add a new `LLMProvider` implementation.
- Propose a new agent tool.
- Improve a prompt template in `prompts/`.
