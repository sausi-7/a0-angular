# packages/shared-types

Generated TypeScript types that mirror the FastAPI Pydantic models.

## How it works

A build step runs `python -m app.export_openapi > openapi.json` in `apps/api`, then `openapi-typescript openapi.json -o index.ts` writes the TS types here. `apps/web` imports them as `@a0-angular/shared-types`.

## Status

Phase 0: placeholder. Codegen pipeline lands in Phase 1 alongside the first real API surface.
