"""
Admin Scraping & API Key Management API
Allows admin to view/update API keys and trigger scraping jobs
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Optional
import os

router = APIRouter(prefix="/api/admin/scraping", tags=["admin-scraping"])

# In production, use secure storage (env vars, vault, or encrypted DB)
API_KEYS = {
    "twitter": os.environ.get("TWITTER_API_KEY", ""),
    "newsapi": os.environ.get("NEWSAPI_API_KEY", ""),
    "reddit_client_id": os.environ.get("REDDIT_CLIENT_ID", ""),
    "reddit_client_secret": os.environ.get("REDDIT_CLIENT_SECRET", ""),
    "reddit_user_agent": os.environ.get("REDDIT_USER_AGENT", "ReputationAI/1.0"),
}

class APIKeyUpdateRequest(BaseModel):
    twitter: Optional[str]
    newsapi: Optional[str]
    reddit_client_id: Optional[str]
    reddit_client_secret: Optional[str]
    reddit_user_agent: Optional[str]

@router.get("/keys", response_model=Dict[str, str])
def get_api_keys():
    # Return current API keys (mask sensitive values)
    return {k: (v[:4] + "****" if v else "") for k, v in API_KEYS.items()}

@router.post("/keys/update")
def update_api_keys(update: APIKeyUpdateRequest):
    # Update API keys in memory (in production, persist securely)
    for k, v in update.dict(exclude_unset=True).items():
        if v:
            API_KEYS[k] = v
    return {"success": True, "message": "API keys updated."}

@router.post("/trigger")
def trigger_scraping_job(source: str, entity: str):
    # Placeholder: In production, enqueue a scraping job (e.g., Celery, RQ)
    # Here, just log the request
    print(f"[ADMIN] Triggered scraping for source={source}, entity={entity}")
    return {"success": True, "message": f"Scraping triggered for {source} and {entity}"}

@router.get("/status")
def get_scraping_status():
    # Placeholder: Return dummy scraping status/logs
    return {
        "last_run": "2026-01-10T12:00:00Z",
        "status": "idle",
        "logs": [
            "2026-01-10T12:00:00Z: Twitter scraping completed (12 mentions)",
            "2026-01-10T11:45:00Z: Reddit scraping completed (8 mentions)",
            "2026-01-10T11:30:00Z: NewsAPI scraping failed (API key missing)"
        ]
    }
