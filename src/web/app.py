"""FastAPI application entry point."""

import os
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from crypto_utils import decrypt_value, encrypt_value
from user_state_store import init_db
from web.routes import ROUTERS

logger = structlog.get_logger()


def _env_flag(name: str, default: bool = False) -> bool:
    """Parse a boolean env flag with a conservative default."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _verify_secret_key() -> None:
    """Canary check: encrypt+decrypt roundtrip with SECRET_KEY on startup."""
    key = os.getenv("SECRET_KEY")
    if not key:
        logger.critical("SECRET_KEY env var not set")
        raise RuntimeError("SECRET_KEY required")
    canary = "canary-check"
    enc = encrypt_value(key, canary)
    dec = decrypt_value(key, enc, key_name="canary")
    if dec != canary:
        logger.critical("SECRET_KEY canary failed — key may have changed")
        raise RuntimeError("SECRET_KEY canary failed")
    logger.info("crypto.canary_ok")


def _start_intel_scheduler():
    """Start background intel scheduler (daily 6am scrape)."""
    if _env_flag("DISABLE_INTEL_SCHEDULER"):
        logger.info("intel_scheduler.disabled")
        return None

    try:
        from intelligence.scheduler import IntelScheduler
        from web.deps import get_config, get_intel_storage

        config = get_config()
        full = config.to_dict()
        storage = get_intel_storage()

        scheduler = IntelScheduler(
            storage=storage,
            config=full.get("sources", {}),
            full_config=full,
        )
        cron = full.get("schedule", {}).get("intelligence_gather", "0 6 * * *")
        scheduler.start(cron_expr=cron)
        logger.info("intel_scheduler.started", cron=cron)
        return scheduler
    except Exception as e:
        logger.error("intel_scheduler.start_failed", error=str(e))
        return None


def _startup_services():
    """Initialize process-level web services and return shutdown state."""
    init_db()
    _verify_secret_key()
    scheduler = _start_intel_scheduler()
    logger.info("web.startup")
    return {"scheduler": scheduler}


def _shutdown_services(state: dict | None) -> None:
    """Stop process-level web services started during lifespan."""
    scheduler = (state or {}).get("scheduler")
    if scheduler:
        scheduler.stop()
    logger.info("web.shutdown")


@asynccontextmanager
async def lifespan(app: FastAPI):
    state = _startup_services()
    yield
    _shutdown_services(state)


async def health():
    return {"status": "ok"}


def _configure_cors(app: FastAPI) -> None:
    """Attach CORS middleware using env-driven frontend origin."""
    frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _register_routes(app: FastAPI) -> None:
    """Mount all API routers and health check."""
    for router in ROUTERS:
        app.include_router(router)
    app.add_api_route("/api/health", health, methods=["GET"])

    from web.routes.metrics import get_metrics

    app.add_api_route("/metrics", get_metrics, methods=["GET"])


def create_app() -> FastAPI:
    """Create the FastAPI application with middleware and routes."""
    app = FastAPI(
        title="AI Coach",
        version="0.1.0",
        lifespan=lifespan,
    )
    _configure_cors(app)
    _register_routes(app)

    @app.middleware("http")
    async def degradation_collector_middleware(request: Request, call_next) -> Response:
        from degradation_collector import clear_collector, init_collector

        init_collector()
        try:
            return await call_next(request)
        finally:
            clear_collector()

    @app.middleware("http")
    async def api_version_rewrite(request: Request, call_next) -> Response:
        path = request.scope["path"]
        if path.startswith("/api/v1/"):
            request.scope["path"] = "/api/" + path[8:]
        response = await call_next(request)
        if path.startswith("/api/") and not path.startswith("/api/v1/") and path != "/api/health":
            response.headers["Deprecation"] = "true"
        return response

    return app


app = create_app()
