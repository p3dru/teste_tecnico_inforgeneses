import requests
import json
from fastapi import HTTPException

from app.core.config import settings

# Kestra API URL
# Note: we construct the full trigger URL using settings
KESTRA_API_URL = f"{settings.KESTRA_API_URL}/executions/trigger/dev/fire-inference-flow"

# Credentials from Settings
KESTRA_AUTH = (settings.KESTRA_USER, settings.KESTRA_PASSWORD)

def trigger_fire_detection_flow(file_path: str, report_id: str) -> str:
    """
    Triggers the Kestra Flow for Fire Detection.
    Passes 'file_path' (relative to /shared-data) and 'report_id' as inputs.
    Returns the Execution ID.
    """
    try:
        # Kestra accepts inputs as multipart/form-data
        files = {
            'file_path': (None, file_path),
            'report_id': (None, report_id)
        }
        
        response = requests.post(
            KESTRA_API_URL, 
            files=files,
            auth=KESTRA_AUTH,
            timeout=5
        )
        
        response.raise_for_status()
        
        data = response.json()
        return data.get("id")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to trigger Kestra: {e}")
        # We assume fire-and-forget for now, but in production we might queue this
        # For now, just log and allow the user to receive 202
        return None
