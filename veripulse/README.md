# VeriPulse (MVP Scaffold)

VeriPulse is a Next.js (App Router) trust engine + daily bulletin MVP. This repo is designed to stay separate while connecting to TrustBeacon services via API.

## TrustBeacon integration

Set the following env vars to point at your TrustBeacon backend. The sample health proxy will call `GET /health` on that service.

```
TRUSTBEACON_API_BASE="https://trustbeacon.example.com/api"
TRUSTBEACON_API_KEY=""
```

You can verify connectivity with:

```
GET /api/trustbeacon/health
```

If the TrustBeacon API base/key are missing, the endpoint will return `503 not_configured`.

## Replit auto-deploy (recommended)

1. Create or open your TrustBeacon Replit project.
2. In Replit, connect this Git repository as an external source (GitHub import).
3. Enable auto-deploy/auto-sync so pushes to this repo update the Replit project.

No additional code changes are required beyond the TrustBeacon env vars above.

## Local dev (Replit)

1. Install dependencies: `npm install`
2. Copy `.env.example` to `.env` and fill in `DATABASE_URL`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and TrustBeacon variables.
3. Run migrations + seed: `npm run db:migrate` and `npm run db:seed`
4. Start dev server: `npm run dev`

## Prisma

Run migrations with `npm run db:migrate` and seed with `npm run db:seed`.
