# apps/web — Angular SPA

## Run locally

```bash
cd apps/web
npm install
npm start
```

Open `http://localhost:4200`.

## Run tests

```bash
npm test
```

## Lint / typecheck

```bash
npm run lint
npx tsc --noEmit
```

## Layout

```
src/
  main.ts                 # Bootstrap
  index.html
  styles.scss             # Tailwind entry
  app/
    app.component.ts      # Root, renders <router-outlet>
    app.config.ts         # Providers
    app.routes.ts         # Routes
    pages/home.component.ts
```

Conventions: standalone components, OnPush change detection, Signals, new control flow (`@if` / `@for` / `@switch`). Component selector prefix is `a0`.

Phase 0 scope: hello-world home page that pings the API `/health` endpoint.
