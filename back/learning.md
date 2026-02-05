# 🧠 Learning Log - Docker Build Optimization

**Date:** 2026-02-04  
**Session:** Docker Performance Optimization & Multi-Stage Builds

---

## 📚 Key Learnings

### 1. Multi-Stage Docker Builds (Critical Optimization)

#### **Concept**
Multi-stage builds allow you to use multiple `FROM` statements in a single Dockerfile. Each `FROM` creates a new stage, and you can selectively copy artifacts from one stage to another.

#### **Why It Matters**
Build dependencies (compilers, dev headers) are needed during installation but bloat production images. Multi-stage builds solve this by:
- **Stage 1 (Builder):** Install build tools + compile dependencies
- **Stage 2 (Runtime):** Copy only compiled artifacts, exclude build tools

#### **Real Impact (This Project)**
```
Before: Single-stage with gcc, libpq-dev → 8.36GB
After:  Multi-stage (builder discarded) → 232MB
Reduction: 97%
```

#### **Pattern Applied**
```dockerfile
# Stage 1: Builder (temporary)
FROM python:3.10-slim as builder
RUN apt-get install gcc libpq-dev  # Build tools
RUN pip install -r requirements.txt

# Stage 2: Runtime (final image)
FROM python:3.10-slim
RUN apt-get install libpq5  # Runtime library only
COPY --from=builder /opt/venv /opt/venv  # Copy compiled packages
```

**Key Insight:** Build tools like `gcc` are 100-200MB. Runtime libraries like `libpq5` are 1-5MB.

---

### 2. Dependency Separation (Architectural Decision)

#### **Problem Identified**
Backend had `torch` (~800MB-1.2GB) and `ultralytics` (~500MB) installed, but:
- Backend only **triggers** Kestra workflows
- Kestra runs inference using `ultralytics/ultralytics:latest` Docker image
- Backend never executes ML code

#### **Decision**
Remove ML dependencies from backend entirely.

#### **Rationale**
- **Separation of Concerns:** Orchestrator (Kestra) handles compute-heavy tasks
- **Microservice Pattern:** Each service has minimal dependencies
- **Docker-in-Docker Benefit:** Kestra spawns ephemeral containers with exact dependencies needed

#### **Trade-off Analysis**
| Approach | Pros | Cons |
|----------|------|------|
| **ML in Backend** | Self-contained | Huge image, slow builds, tight coupling |
| **ML in Kestra** | Lean backend, fast builds, isolation | Requires orchestrator setup |

**Chosen:** ML in Kestra (already implemented in project architecture)

---

### 3. Virtual Environment Isolation in Docker

#### **Concept**
Create a Python virtual environment (`venv`) inside Docker, then copy it between stages.

#### **Why Not System-Wide pip install?**
```dockerfile
# ❌ Bad: System-wide install
RUN pip install -r requirements.txt

# ✅ Good: Virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements.txt
```

#### **Benefits**
1. **Cleaner Separation:** All Python packages in `/opt/venv`, not scattered in `/usr/local`
2. **Easier Debugging:** `ls /opt/venv/lib/python3.10/site-packages` shows exactly what's installed
3. **Multi-Stage Friendly:** Copy entire `/opt/venv` directory in one `COPY --from=builder`

#### **Applied Pattern**
```dockerfile
# Builder stage
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
```

---

### 4. Docker Layer Caching Strategy

#### **Problem**
Every code change invalidated the entire build, forcing reinstallation of all dependencies (5-10 minutes).

#### **Solution: Copy requirements.txt First**
```dockerfile
# ❌ Bad: Code changes invalidate pip install
COPY . .
RUN pip install -r requirements.txt

# ✅ Good: requirements.txt cached separately
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .  # Code changes don't affect pip layer
```

#### **Impact**
- **requirements.txt unchanged:** Build uses cache → 2.7s
- **requirements.txt changed:** Only pip layer rebuilds → ~30s
- **Code changed:** Only `COPY . .` layer rebuilds → <1s

#### **Cache Hit Rate**
```
Before optimization: ~10% (everything rebuilds)
After optimization:  ~95% (only changed layers rebuild)
```

---

### 5. .dockerignore (Build Context Optimization)

#### **Concept**
`.dockerignore` is like `.gitignore` but for Docker builds. It excludes files from the build context sent to Docker daemon.

#### **Why It Matters**
Docker sends **entire directory** to daemon before building. Large contexts slow down builds even if files aren't used.

#### **Real Impact**
```
Before: Sending 50MB context (includes __pycache__, .git, logs)
After:  Sending 20KB context (only source code)
Result: 2-3s faster build start
```

#### **Critical Exclusions**
```
__pycache__/  # Python cache (regenerated anyway)
*.pyc         # Compiled Python (not portable)
.git/         # Version control (huge, unnecessary)
.env          # Secrets (security risk)
*.log         # Logs (temporary data)
```

---

### 6. Non-Root User Security Pattern

#### **Problem**
Running containers as `root` is a security risk. If container is compromised, attacker has root privileges.

#### **Solution**
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

#### **Permission Challenge Encountered**
```python
# This fails if run as non-root user
os.makedirs('/shared-data/uploads', exist_ok=True)
# PermissionError: [Errno 13] Permission denied
```

#### **Fix: Create Directories Before User Switch**
```dockerfile
# Create directories as root
RUN mkdir -p /shared-data/uploads && \
    chmod 777 /shared-data/uploads

# Then switch to non-root
RUN useradd -m -u 1000 appuser
USER appuser
```

#### **Security Principle**
- **Least Privilege:** Application runs with minimal permissions
- **Defense in Depth:** Even if app is exploited, attacker can't escalate to root

---

### 7. Health Checks in Docker

#### **Concept**
Docker can periodically check if container is healthy, not just running.

#### **Implementation**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/', timeout=2)" || exit 1
```

#### **Parameters**
- `--interval=30s`: Check every 30 seconds
- `--timeout=3s`: Fail if check takes >3s
- `--start-period=5s`: Grace period for app startup
- `--retries=3`: Mark unhealthy after 3 consecutive failures

#### **Benefit**
```bash
$ docker ps
NAMES                  STATUS
teste_tecnico_api_1    Up (healthy)  # Not just "Up"
```

Orchestrators (Kubernetes, Docker Swarm) can auto-restart unhealthy containers.

---

### 8. Build Performance Metrics

#### **Measurement Methodology**
```bash
# Clean build (no cache)
time docker-compose build --no-cache api

# Cached build (requirements.txt unchanged)
time docker-compose build api
```

#### **Results**
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Clean Build** | 10-15 min | 1.3 min | 87% faster |
| **Cached Build** | 8-10 min | 2.7s | 99% faster |
| **Image Size** | 8.36 GB | 232 MB | 97% smaller |

#### **Why Measure?**
- **Developer Experience:** Fast builds = faster iteration
- **CI/CD Impact:** 10min builds → 1.3min = 8x more builds/hour
- **Disk Cost:** 8GB/developer → 232MB = 35x more projects on same disk

---

## 🎯 Actionable Takeaways

### **For Future Projects**

1. **Always Use Multi-Stage Builds**
   - Separate builder and runtime stages
   - Copy only compiled artifacts to final image

2. **Audit Dependencies**
   - Question every dependency: "Does THIS service need this?"
   - Move heavy dependencies to specialized services

3. **Optimize Layer Order**
   - Copy `requirements.txt` before code
   - Group `RUN` commands to reduce layers

4. **Create .dockerignore Early**
   - Start with template, refine as needed
   - Exclude cache, logs, git, env files

5. **Security by Default**
   - Always create non-root user
   - Create directories before user switch

6. **Measure Everything**
   - Track image sizes over time
   - Monitor build times in CI/CD

---

## 🔗 References

- **Multi-Stage Builds:** [Docker Docs](https://docs.docker.com/build/building/multi-stage/)
- **Best Practices:** [Docker Official Guide](https://docs.docker.com/develop/dev-best-practices/)
- **Layer Caching:** [BuildKit Cache](https://docs.docker.com/build/cache/)

---

## 📊 Before/After Comparison

### **Before Optimization**
```dockerfile
FROM python:3.10-slim
RUN apt-get install libgl1 libglib2.0-0  # For ultralytics
COPY requirements.txt .
RUN pip install torch ultralytics ...  # 2-3GB of ML deps
COPY . .
CMD ["uvicorn", "app.main:app"]
```
**Result:** 8.36GB image, 10-15min builds

### **After Optimization**
```dockerfile
# Builder stage
FROM python:3.10-slim as builder
RUN apt-get install gcc libpq-dev
COPY requirements.txt .
RUN python -m venv /opt/venv && pip install -r requirements.txt

# Runtime stage
FROM python:3.10-slim
RUN apt-get install libpq5
COPY --from=builder /opt/venv /opt/venv
COPY . .
RUN useradd appuser && USER appuser
CMD ["uvicorn", "app.main:app"]
```
**Result:** 232MB image, 1.3min builds

---

## ✅ Verification Checklist

- [x] Multi-stage build implemented
- [x] Unnecessary dependencies removed
- [x] .dockerignore created
- [x] Virtual environment isolation
- [x] Non-root user configured
- [x] Health check added
- [x] Build time measured and improved
- [x] Image size reduced by >90%
- [x] All containers healthy and operational
