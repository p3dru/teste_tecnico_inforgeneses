from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
