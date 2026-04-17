# Prompt templates

Prompt templates that the agent loop uses live here as `.md` and `.yaml` files.

Editing a prompt does not require Python or Angular knowledge — it is the lowest-friction way to contribute. Open a PR with your change and a one-line "why" in the description.

## Status

Phase 0: empty. The first templates land in Phase 1 alongside the agent loop.

## Conventions (proposed, will be enforced by CI in Phase 1)

- One template per file. Filename describes the role: `system_angular.md`, `tool_use_examples.yaml`.
- Markdown for free-form prose; YAML when the prompt has multiple slots the loop fills in.
- Keep templates under 300 lines. Long prompts are usually a sign that something belongs in code.
