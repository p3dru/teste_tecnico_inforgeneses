import requests
import json
from fastapi import HTTPException

# Kestra API URL (Service name 'kestra' is resolvable inside Docker network)
KESTRA_API_URL = "http://kestra:8080/api/v1/executions/trigger/dev/fire-inference-flow"

# Default Credentials (as per barriers.md)
KESTRA_AUTH = ("admin@kestra.io", "Admin1234")

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
