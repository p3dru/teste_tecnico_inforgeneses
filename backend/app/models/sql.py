from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class ReportStatus(str, enum.Enum):
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    ERROR = "ERROR"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, index=True)  # UUID stored as string
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(String, default=ReportStatus.PROCESSING.value) # Use string for simplicity with async drivers
    created_at = Column(DateTime, default=datetime.utcnow)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    # Summary of findings (e.g., {"fire_detected": true}) stored as simple string/json if needed in SQL
    # but detailed logs go to Mongo
