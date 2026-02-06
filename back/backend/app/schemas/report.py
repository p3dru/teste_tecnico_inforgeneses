from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

class ReportBase(BaseModel):
    file_path: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ReportResponse(ReportBase):
    id: str
    user_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    class_name: str
    class_id: Optional[int] = None

class ReportDetail(ReportResponse):
    detections: List[BoundingBox] = []
    model_version: Optional[str] = None
    processing_time_ms: Optional[float] = None
