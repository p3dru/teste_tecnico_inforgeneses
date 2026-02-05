from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.api import deps
from app.db.session import get_db
from app.models.sql import Report, User
from app.schemas.report import ReportResponse

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
    query = select(Report).order_by(desc(Report.created_at)).offset(skip).limit(limit)
    
    if status:
        query = query.where(Report.status == status)
        
    result = await db.execute(query)
    reports = result.scalars().all()
    
    return reports
