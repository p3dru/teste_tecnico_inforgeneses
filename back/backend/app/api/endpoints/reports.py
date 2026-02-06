from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.api import deps
from app.db.session import get_db
from app.models.sql import Report, User
from app.models.nosql import InferenceLog
from app.schemas.report import ReportResponse, ReportDetail

router = APIRouter()

@router.get("/", response_model=List[ReportResponse])
async def read_reports(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve reports.
    - Pagination: skip, limit
    - Filters: status (PROCESSING, DONE, ERROR)
    - Returns newest first.
    """
    # Filter by current user for isolation
    query = select(Report).where(Report.user_id == current_user.id).order_by(desc(Report.created_at)).offset(skip).limit(limit)
    
    if status:
        query = query.where(Report.status == status)
        
    result = await db.execute(query)
    reports = result.scalars().all()
    
    return reports

@router.get("/{report_id}", response_model=ReportDetail)
async def read_report_detail(
    report_id: str,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed report with detections.
    1. Fetch Report from SQL (check ownership).
    2. Fetch InferenceLog from Mongo.
    3. Return combined data.
    """
    # 1. Fetch from SQL (and verify ownership)
    result = await db.execute(select(Report).where(Report.id == report_id, Report.user_id == current_user.id))
    report = result.scalars().first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    # 2. Fetch from Mongo
    log = await InferenceLog.find_one(InferenceLog.report_id == report_id)
    
    detections = []
    model_version = None
    processing_time_ms = 0.0
    
    if log:
        # Fix: Map Kestra 'name' to Schema 'class_name'
        detections = [
            {
                "x1": d.get("x1"),
                "y1": d.get("y1"),
                "x2": d.get("x2"),
                "y2": d.get("y2"),
                "confidence": d.get("confidence"),
                "class_name": d.get("name"),  # Map name -> class_name
                "class_id": d.get("class")    # Preserve ID if needed
            }
            for d in log.detections
        ]
        model_version = log.model_version
        processing_time_ms = log.processing_time_ms
        
    # 3. Combine
    return ReportDetail(
        **report.__dict__,
        detections=detections,
        model_version=model_version,
        processing_time_ms=processing_time_ms
    )
