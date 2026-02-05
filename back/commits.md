# Commit Log

## [Uncommitted] Security & Configuration Hardening
**Date:** 2026-02-05
**Changes:**
- **Configuration**: Created `.env` (and `.env.example`) for secure credential management.
- **Refactor**: Migrated `backend` to use `pydantic-settings` for robust environment validation.
- **Cleanup**: Removed hardcoded secrets from `config.py`, `kestra_client.py` and `register_flows.sh`.
- **Scripts**: Updated helper scripts to source `.env` file automatically.

**Suggested Message:**
\`\`\`bash
chore: implement secure configuration with pydantic-settings and dotenv

- Create .env and .env.example
- Migrate backend config to Pydantic BaseSettings
- Remove hardcoded credentials from codebase
- Update scripts to source environment variables
\`\`\`

---

## [Uncommitted] Project Documentation Update
**Date:** 2026-02-05
**Changes:**
- **Documentation**: Rewrote `README.md` with "Manual Setup" guide for Kestra flows (due to Auth barrier).
- Added "Guia de Instalação", "Configuração Manual" and updated "Status do Projeto" to reflect Frontend completion.

**Suggested Message:**
\`\`\`bash
docs: update readme with manual setup instructions

- Rewrite README to serve as single source of truth
- Add manual Kestra flow registration steps
- Update project status and architecture diagrams
\`\`\`

---

## [Uncommitted] AI Model Integration & System Reset
**Date:** 2026-02-05
**Changes:**
- **Infrastructure**: Performed full system reset (wiped volumes/containers) to verify clean install.
- **AI Model**: Implemented simulated custom model workflow.
    - Generated `custom_fire_model.pt` in `/shared-data/models`.
    - Updated `fire_inference.yaml` to prioritize custom model path.
- **Barriers**: Documented Kestra Auth persistence issue in `barriers.md`.

**Suggested Message:**
\`\`\`bash
feat: integrate custom ai model and reset infrastructure

- Generate simulated custom YOLO model in shared volume
- Update Kestra flow to use custom model path
- Document Kestra auth barriers
\`\`\`

---

## [Uncommitted] Frontend Visualization & Charts
**Date:** 2026-02-05
**Changes:**
- Implemented `ReportDetailPage` with Image + Bounding Box visualization (responsive percentages).
- Implemented `StatsChart` component using `chart.js` (Doughnut & Bar charts).
- Updated Dashboard to include charts and link to report details.
- Updated Backend to serve static files (images) from `/shared-data/uploads`.
- Implemented `GET /reports/{id}` endpoint to fetch combined SQL + Mongo data.

**Suggested Message:**
\`\`\`bash
feat: implement frontend visualization with bounding boxes and charts
\`\`\`

---

## [Uncommitted] Upload Fix & Report Isolation
**Date:** 2026-02-05
**Changes:**
- Fixed 500 Error in `/upload` by correcting Docker volume permissions (chmod 777 on shared volume).
- Implemented User Isolation in `/reports`: users now only see their own reports.
- Added `tests/test_upload_debug.py` script for reproduction.

**Suggested Message:**
\`\`\`bash
fix: resolve upload permission error and implement report user isolation
\`\`\`

---

## [Uncommitted] Docker Build Optimization
**Date:** 2026-02-04
**Changes:**
- Implemented multi-stage Dockerfile with builder and runtime stages.
- Removed `torch` and `ultralytics` from `backend/requirements.txt` (~2GB reduction).
- Created `backend/.dockerignore` to exclude unnecessary files from build context.
- Added virtual environment isolation in Docker build process.
- Fixed permission issues for `/shared-data/uploads` directory.
- Configured non-root user (appuser) for security.
- Added health check to API container.

**Impact:**
- Image size reduced from 8.36GB to 232MB (97% reduction).
- Clean build time reduced from 10-15min to 1.3min (87% faster).
- Cached build time reduced to 2.7s (99% faster).

**Suggested Message:**
```bash
perf: optimize docker build with multi-stage and remove ml dependencies

- Implement multi-stage Dockerfile (builder + runtime)
- Remove torch and ultralytics from backend (handled by Kestra)
- Add .dockerignore for better cache utilization
- Configure non-root user and health checks
- Reduce image size from 8.36GB to 232MB (97% reduction)
- Improve build times: clean 1.3min, cached 2.7s
```

---

## [Uncommitted] Project Documentation & Fixes
**Date:** 2026-02-04
**Changes:**
- Created `README.md` with beginner-friendly setup and usage instructions.
- Fixed `kestra/flows/fire_inference.yaml` validation error (added `database` field).
- Fixed `backend/app/api/endpoints/upload.py` syntax error (restored file content).
- Pinned `bcrypt==3.2.2` in `requirements.txt` to fix Passlib 72-byte limit bug.

**Suggested Message:**
```bash
docs: add readme and fix dependencies
```

---

## [Uncommitted] Reports Retrieval Module
**Date:** 2026-02-04
**Changes:**
- Implemented `backend/app/api/endpoints/reports.py` (GET /reports with pagination).
- Registered Reports Router in `main.py`.

**Suggested Message:**
```bash
feat: implement reports retrieval endpoint with pagination and filtering
```

---

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
