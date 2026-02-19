"""FastAPI application entry point."""

import os
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from web.routes import advisor, goals, intel, journal, research, settings

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
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


@app.get("/api/health")
async def health():
    return {"status": "ok"}
