# Commit Log

## [Uncommitted] Kestra Pipeline Implementation
**Date:** 2026-02-04
**Changes:**
- Created `kestra/flows/fire_inference.yaml` orchestrating Docker Inference, SQL Update, and Mongo Log.
- Embedded Python script with `ultralytics` YOLO inference.
- Added `backend/scripts/register_flows.sh` (Manual registration Helper).
- Updated `docker-compose.yml` configuration (attempted auth fix).

**Suggested Message:**
```bash
feat: implement kestra fire inference flow and registration scripts
```

---

## [Uncommitted] Kestra Client & Upload Integration
**Date:** 2026-02-04
**Changes:**
- Implemented `backend/app/core/kestra_client.py` using `requests` to trigger flows.
- Updated `backend/app/api/endpoints/upload.py` to trigger Kestra flow after file save.
- Registered Upload Router in `main.py` under the `/files` prefix.

**Suggested Message:**
```bash
feat: implement kestra http client and integrate with upload workflow
```

---

## [Uncommitted] File Upload Module Implementation
**Date:** 2026-02-04
**Changes:**
- Created `backend/app/schemas/report.py` (ReportResponse models).
- Implemented `backend/app/api/endpoints/upload.py` (File Handling, Disk Save, SQL Insert).
- Configured shared volume path `/shared-data/uploads`.

**Suggested Message:**
```bash
feat: implement file upload endpoint with disk storage and db logging
```

---

## [Uncommitted] Authentication Module Implementation
**Date:** 2026-02-04
**Changes:**
- Implemented `backend/app/core/security.py` (Password Hashing, JWT utils).
- Created `backend/app/schemas/auth.py` (Token, UserCreate models).
- Implemented `backend/app/api/deps.py` (Current User dependency).
- Created `backend/app/api/endpoints/auth.py` (Login / Signup controllers).
- Registered Auth Router in `main.py`.

**Suggested Message:**
```bash
feat: implement jwt authentication and user management endpoints
```

---

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
