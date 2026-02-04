# Commit Log

## [Uncommitted] Database Layer Implementation
**Date:** 2026-02-04
**Changes:**
- Implemented SQLAlchemy Async Models (`User`, `Report`) for PostgreSQL.
- Implemented Beanie/Motor ODM Models (`InferenceLog`) for MongoDB.
- Configured async Database Sessions and Settings (`config.py`).
- Updated `docker-compose.yml` to use `postgresql+asyncpg` protocol.
- Updated `backend/requirements.txt` with `asyncpg`, `sqlalchemy`, `beanie`.
- Added DB initialization hook in `backend/app/main.py`.

**Suggested Message:**
```bash
feat: implement async db layer with postgres and mongodb models
```

---

## [Uncommitted] Infrastructure Setup
**Date:** 2026-02-02
**Changes:**
- Created `docker-compose.yml` orchestrating Postgres, Mongo, Kestra, and API.
- Created `backend/Dockerfile` with Python 3.10 and system dependencies.
- Created `backend/requirements.txt` with PyTorch (CPU), FastAPI, and DB drivers.
- Created `backend/app/main.py` as a minimal entry point.
- Created `kestra/flows/hello_world.yaml` for environment verification.
- Configured shared Docker volume `/shared-data` for Kestra/API integration.

**Suggested Message:**
```bash
feat: add initial docker infrastructure and kestra hello world flow
```
