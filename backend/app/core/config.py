import os

class Settings:
    PROJECT_NAME: str = "Wildfire Detection API"
    
    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkeyForDevOnlyChangeInProd")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Databases
    # Note: 'postgres' is the service name in docker-compose
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@postgres/wildfire_db")
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://user:password@mongo:27017")
    MONGO_DB_NAME: str = "wildfire_logs"

settings = Settings()
