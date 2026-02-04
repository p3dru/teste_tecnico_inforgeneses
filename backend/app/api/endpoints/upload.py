import os
import shutil
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.db.session import get_db
from app.models.sql import User, Report, ReportStatus
from app.schemas.report import ReportResponse
from app.core.kestra_client import trigger_fire_detection_flow

router = APIRouter()

UPLOAD_DIR = "/shared-data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=ReportResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_image(
    file: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload an image for wildfire detection.
    
    1. Validates file type.
    2. Saves file to shared volume.
    3. Creates initial DB record.
    4. Triggers Kestra.
    """
    
    # 1. Validation
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # 2. Save to Disk (Shared Volume)
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    safe_filename = f"{file_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
        
    # 3. Create DB Record
    report = Report(
        id=file_id,
        user_id=current_user.id,
        file_path=safe_filename,
        status=ReportStatus.PROCESSING.value,
        latitude=latitude,
        longitude=longitude
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    
    # 4. Trigger Kestra
    execution_id = trigger_fire_detection_flow(file_path=safe_filename, report_id=file_id)
    if execution_id:
        print(f"[{file_id}] Started Kestra Execution: {execution_id}")
    else:
        print(f"[{file_id}] Warning: Could not trigger Kestra flow.")
    
    return report
