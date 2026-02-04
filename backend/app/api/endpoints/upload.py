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

    # 4. Trigger Kestra
    execution_id = trigger_fire_detection_flow(file_path=safe_filename, report_id=file_id)
    if execution_id:
        print(f"Started Kestra Execution: {execution_id}")
    
    return report
