# Contributing to A0 for Angular

Thanks for wanting to help. This is a young project; your contribution has a disproportionately large impact right now.

## Ground rules

- Be kind. We follow the [Contributor Covenant](CODE_OF_CONDUCT.md).
- Small, focused PRs merge faster than large ones. If your change is >500 lines, open a draft issue first so we can agree on the shape.
- Discussion happens in GitHub Discussions and Issues. Don't DM maintainers.

## Ways to contribute (ranked by easiest first)

1. **Docs & typos.** Any doc improvement is welcome, no issue needed.
2. **Prompt templates.** They live in `packages/agent-core/prompts/` as `.md` / `.yaml`. Editing these does not require knowing Python or Angular.
3. **Angular schematic tools.** Add a new tool the agent can call (e.g. "generate a reactive form", "wire a route guard"). See `packages/ng-schematics/README.md`.
4. **LLM provider adapters.** Add support for a new provider behind the `LLMProvider` interface. See `packages/agent-core/providers/`.
5. **Bugs.** Grab a [good first issue](https://github.com/sausi-7/a0-angular/labels/good%20first%20issue).
6. **Features.** Check [ROADMAP.md](ROADMAP.md) and comment on the relevant issue before starting.

## Dev setup

Prereqs: Node 20+, Python 3.12+, [uv](https://github.com/astral-sh/uv). No Docker required.

```bash
git clone https://github.com/sausi-7/a0-angular.git

cd a0-angular
make install   # installs api (uv) and web (npm) deps
make dev       # runs api (:8000) and web (:4200) in parallel
make test      # backend + frontend unit tests
make lint      # ruff, mypy, eslint, tsc
```

Need just one side? `make dev-api` or `make dev-web`. Prefer Docker? `make dev-docker` runs the same stack via `docker compose`.

Per-app commands live in `apps/api/README.md` and `apps/web/package.json`.

## PR checklist

- [ ] Rebased on `main`.
- [ ] `make lint` and `make test` pass locally.
- [ ] New behavior has a test (unit or E2E).
- [ ] Docs updated if user-facing behavior changed.
- [ ] PR description explains *why*, not just *what*.

## Commit messages

Conventional Commits preferred but not required:

```
feat(agent): add edit_file tool for structured diffs
fix(web): streaming buffer drops last token
docs(adr): record BYOK decision
```

## Code style

- Python: `ruff format`, `ruff check`, `mypy --strict`. Configured in `pyproject.toml`.
- TypeScript: ESLint + Prettier. Configured in `apps/web/`.
- Angular: standalone components, Signals, new control flow. No `NgModule`s in new code.

## Architecture Decision Records

Before making a decision with long-term impact (new dep, new surface, new protocol), open an ADR under `docs/adr/`. Use the template in `docs/adr/0000-template.md`. It's OK to propose one in a PR.

## Review process

- One maintainer review is enough for docs, prompts, schematic tools.
- Two reviews for anything touching the agent loop, auth, or file-write paths.
- Maintainers aim to respond within 3 business days. Ping in Discussions if we forget.

## Releasing

Maintainers only. We cut releases from `main` using tags `vX.Y.Z`. Changelog is auto-generated from Conventional Commits.

## Security

Please do not open public issues for security bugs. See [SECURITY.md](SECURITY.md).
