# Architecture

The frontend is a TypeScript React/Vite PWA. `src/lib/db.ts` is the local persistence boundary; `src/lib/validation.ts` is the untrusted JSON boundary; practice is a local state machine over a stored pack. The FastAPI backend exposes public published-pack reads and protected teacher writes over a SQLAlchemy model. Demo JSON is shared as a reviewable content source and seeded into SQLite at startup.
