# A0 for Angular

> Open-source vibe-coding platform for Angular apps. Describe an app in plain English, get a working Angular project you can run, edit, and ship.

A0 for Angular is what Lovable, Bolt, and v0 are for React — but purpose-built for Angular. Generated code follows modern Angular conventions by default: standalone components, Signals, the new control flow (`@if` / `@for` / `@switch`), functional guards, and dependency injection the idiomatic way.

## Status

**Phase 0 — Foundation.** The repo is being set up; no features yet. Contributions welcome from day one. See [ROADMAP.md](ROADMAP.md).

## Features (planned)

- Chat-driven generation of real Angular projects (not snippets — full apps)
- Live preview via a local `ng serve`
- Streaming edits with file-level diffs
- Bring Your Own Key: Anthropic, OpenAI, OpenRouter
- Self-hostable with `make dev` (Docker optional)
- Plugin seams for new LLM providers, sandbox backends, and schematics

## Quickstart (self-host)

> Prerequisites: Node 20+, Python 3.12+, [uv](https://github.com/astral-sh/uv). No Docker needed.

```bash
git clone https://github.com/sausi-7/a0-angular.git

cd a0-angular
make install
make dev
```

Then open `http://localhost:4200` for the web UI and `http://localhost:8000/docs` for the API.

For the demo slice, `POST http://localhost:8000/demo/start` seeds `workspace/demo/` from the starter template and brings the preview up on port `4300`.

**Prefer Docker?** `make dev-docker` runs the full stack via `docker compose` instead. Docker is optional — both paths are supported.

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full picture. Short version: Angular SPA talks to a FastAPI backend over REST + WebSockets; the backend runs an LLM agent loop that reads and writes files in a local `workspace/` directory; a sidecar `ng serve` serves the generated app to an iframe in the SPA.

## Contributing

We want contributors from day one. Start here:

- [CONTRIBUTING.md](CONTRIBUTING.md) — dev setup, PR workflow, how we review
- [PLAN.md](PLAN.md) — phased plan with concrete epics and issues you can claim
- [Good first issues](https://github.com/sausi-7/a0-angular/labels/good%20first%20issue) — curated on-ramps
- [docs/adr/](docs/adr/) — architecture decisions, so you can argue with them

Ways to help that don't require writing the hard parts:
- Improve prompt templates (they live as `.md` / `.yaml`, not code)
- Add an LLM provider adapter
- Add an Angular schematic tool the agent can call
- Improve docs, write a tutorial, share a demo

## License

[MIT](LICENSE).

## Acknowledgements

Inspired by the excellent work of the Lovable, Bolt, and v0 teams. This project exists because Angular deserves the same.
