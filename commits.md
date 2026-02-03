# Commit Log

## [Uncommitted] Infrastructure Setup
**Date:** 2026-02-02
**Changes:**
- Created `docker-compose.yml` orchestrating Postgres, Mongo, Kestra, and API.
- Created `backend/Dockerfile` with Python 3.10 and system dependencies.
- Created `backend/requirements.txt` with PyTorch (CPU), FastAPI, and DB drivers.
- Created `backend/app/main.py` as a minimal entry point.
- Configured shared Docker volume `/shared-data` for Kestra/API integration.

**Suggested Message:**
```bash
feat: add initial docker infrastructure with kestra, db and backend skeleton
```
