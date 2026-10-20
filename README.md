# OfflineMock

OfflineMock is an offline-first practice app for secondary-school learners. It includes small demo packs, immediate feedback, step-by-step explanations, English and Nigerian Pidgin variants, local progress, accessible preferences, and a FastAPI catalogue service.

## Run locally

```bash
cp .env.example .env
npm install
npm run dev
```

The frontend runs at `http://localhost:5173`. In another terminal:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload --port 8000
```

The bundled demo packs work without the API. The API uses SQLite locally and accepts a PostgreSQL `DATABASE_URL` in deployment.

## Tests and builds

```bash
npm run validate-content
npm test
npm run build
cd backend && pytest
```

The production build measured an app shell of approximately 115 KB gzip JavaScript plus 3 KB gzip CSS; downloaded packs are excluded.

## Offline workflow

Open the app once, visit **Packs**, and download or import a pack. Practice, explanations, preferences, and results are then available from IndexedDB without a network. The service worker caches the app shell. Production installation requires HTTPS; localhost is supported for development.

## Teacher workflow and security

Use **Teacher studio** to draft metadata and export a complete JSON pack. Imported files are validated with Zod and never executed as code. API write routes require `X-Teacher-Key` matching `TEACHER_API_KEY`. Replace the development secret and add a real identity provider, HTTPS, rate limiting, secret management, and database backups before public deployment.

Anonymous student practice stays local in this MVP; no progress sync or student identity is created. Pidgin strings are demo content clearly marked for local review. See `docs/` for architecture, offline, accessibility, and deployment notes.