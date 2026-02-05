import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Wildfire Detection API"
    
    # Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Databases
    DATABASE_URL: str
    MONGO_URL: str
    MONGO_DB_NAME: str = "wildfire_logs"
    
    # Kestra Integration
    KESTRA_API_URL: str = "http://kestra:8080/api/v1"
    KESTRA_USER: str
    KESTRA_PASSWORD: str

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
