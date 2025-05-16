from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class HealthCheckResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    details: Dict[str, Any]

@router.get(
    "",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the API is running and healthy.",
)
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint that returns the current status of the API.
    """
    import time
    from datetime import datetime
    import platform
    import psutil
    
    # Basic system information
    system_info = {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent,
    }
    
    # Application information
    app_info = {
        "name": "BigQuery Text-to-SQL API",
        "status": "healthy",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    
    # Log the health check
    logger.info("Health check requested", system_info=system_info)
    
    return HealthCheckResponse(
        status="ok",
        version=app_info["version"],
        timestamp=app_info["timestamp"],
        details={
            "app": app_info,
            "system": system_info,
        },
    )
