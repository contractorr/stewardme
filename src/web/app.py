"""FastAPI application entry point."""

import os
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from web.routes import (
    advisor,
    briefing,
    engagement,
    goals,
    intel,
    journal,
    learning,
    onboarding,
    profile,
    projects,
    research,
    settings,
    trends,
)
from web.user_store import init_db

logger = structlog.get_logger()


def _verify_secret_key() -> None:
    """Canary check: encrypt+decrypt roundtrip with SECRET_KEY on startup."""
    key = os.getenv("SECRET_KEY")
    if not key:
        logger.critical("SECRET_KEY env var not set")
        raise RuntimeError("SECRET_KEY required")
    from web.crypto import decrypt_value, encrypt_value

    canary = "canary-check"
    enc = encrypt_value(key, canary)
    dec = decrypt_value(key, enc, key_name="canary")
    if dec != canary:
        logger.critical("SECRET_KEY canary failed — key may have changed")
        raise RuntimeError("SECRET_KEY canary failed")
    logger.info("crypto.canary_ok")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    _verify_secret_key()
    logger.info("web.startup")
    yield
    logger.info("web.shutdown")


app = FastAPI(
    title="AI Coach",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow frontend origin
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(settings.router)
app.include_router(journal.router)
app.include_router(advisor.router)
app.include_router(goals.router)
app.include_router(intel.router)
app.include_router(research.router)
app.include_router(onboarding.router)
app.include_router(briefing.router)
app.include_router(trends.router)
app.include_router(learning.router)
app.include_router(projects.router)
app.include_router(engagement.router)
app.include_router(profile.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
