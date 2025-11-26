# deps.py
from fastapi_limiter import FastAPILimiter
import redis.asyncio as aioredis
import os

async def init_limiter():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Create redis client using the new interface
    redis_client = aioredis.from_url(
        redis_url,
        encoding="utf-8",
        decode_responses=True
    )
    
    # Initialize FastAPI-Limiter with the new client
    await FastAPILimiter.init(redis_client)
