# app/auth.py
import os
import secrets
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy import select
from .models import ApiKey
from .database import AsyncSessionLocal

API_KEY_HEADER = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)

MASTER_API_KEY = os.getenv("MASTER_API_KEY", "changeme_master_key")

# Validate API key against DB
async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    async with AsyncSessionLocal() as session:
        q = select(ApiKey).where(ApiKey.key == api_key, ApiKey.revoked == 0)
        res = await session.execute(q)
        key_obj = res.scalar_one_or_none()
        if not key_obj:
            raise HTTPException(status_code=401, detail="Invalid or revoked API key")
        return key_obj

# Admin route protection using MASTER_API_KEY header
async def require_master_key(x_master_key: str = Security(api_key_header)):
    if x_master_key != MASTER_API_KEY:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return True

# Helper to create an API key
def generate_api_key():
    return secrets.token_urlsafe(32)
