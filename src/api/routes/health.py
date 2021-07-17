from functools import lru_cache
from fastapi import APIRouter, Depends

from ...config import Settings

router = APIRouter()

@lru_cache()
def get_settings():
    return Settings()

@router.get("/")
def api_health(config: Settings = Depends(get_settings)):
    """Check api status"""
    return {
        "API =>": f"[{config.app_name} {config.version}]",
        "ENV =>": f"({config.app_env})",
        "STATUS =>": "OK",
    }