# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi_limiter import FastAPILimiter
from .database import engine, Base
from .routes import accounts, transactions
from .deps import init_limiter
from dotenv import load_dotenv
import asyncio

load_dotenv()

app = FastAPI(title="MockBank API", description="A simple mock banking API", version="1.0.0")

# Register routers
app.include_router(accounts.router)
app.include_router(transactions.router)

# Force HTTPS only in production (enable middleware if you set FORCE_HTTPS=1)
if os.getenv("FORCE_HTTPS", "0") == "1":
    app.add_middleware(HTTPSRedirectMiddleware)

@app.on_event("startup")
async def on_startup():
    # create DB tables if they don't exist (simple approach)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # init rate limiter if redis configured
    try:
        await init_limiter()
    except Exception as e:
        # If Redis is not available the limiter will not be active
        print("Warning: Could not initialize rate limiter (Redis). Error:", e)

@app.get("/")
async def root():
    return {"message": "MockBank API running. Docs at /docs"}
