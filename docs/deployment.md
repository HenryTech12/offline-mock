# Deployment

Build the frontend with `npm run build` and serve `frontend/dist` from an HTTPS static host. Run the API with `uvicorn app.main:app --host 0.0.0.0 --port 8000` or use the included Docker Compose file. Set `DATABASE_URL`, `CORS_ORIGINS`, and a strong secret `TEACHER_API_KEY` in a deployment secret store. Use PostgreSQL for production, terminate TLS at the platform, and add an identity provider, rate limiting, structured logs, and backups before public teacher publishing.
