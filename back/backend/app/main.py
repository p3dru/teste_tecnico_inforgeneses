from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import init_sql_db, init_mongo_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Initializing Databases...")
    await init_sql_db()
    await init_mongo_db()
    yield
    # Shutdown
    print("Shutting down...")

from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings

app = FastAPI(title="Wildfire Detection API", lifespan=lifespan)

# Mount /static/uploads to point to /shared-data/uploads (configurable for tests)
SHARED_UPLOADS_DIR = os.getenv("SHARED_UPLOADS_DIR", "/shared-data/uploads")
os.makedirs(SHARED_UPLOADS_DIR, exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory=SHARED_UPLOADS_DIR), name="uploads")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.endpoints import auth, upload, reports
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(upload.router, prefix="/files", tags=["files"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Wildfire Detection API"}
