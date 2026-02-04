from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, List, Any

class BoundingBox(Document):
    # Embedded document for bounding box details
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    class_name: str

class InferenceLog(Document):
    """
    Stores the raw heavy output from the ML model.
    Linked to the SQL Report via report_id.
    """
    report_id: str = Field(..., index=True) # References Report.id (UUID)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Raw YOLO output details
    fire_confidence: float = 0.0
    smoke_confidence: float = 0.0
    detections: List[dict] = [] # List of BoundingBox dicts
    
    # Metadata about the execution environment
    model_version: str = "yolov8"
    processing_time_ms: float = 0.0

    class Settings:
        name = "inference_logs"
