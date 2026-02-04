from fastapi import FastAPI
from contextlib import asynccontextmanager
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

app = FastAPI(title="Wildfire Detection API", lifespan=lifespan)

from app.api.endpoints import auth, upload
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(upload.router, prefix="/files", tags=["files"])

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Wildfire Detection API"}
