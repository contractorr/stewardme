"""API key and settings management routes (per-user)."""

import structlog
from fastapi import APIRouter, Depends, HTTPException

from web.auth import get_current_user
from web.deps import get_secret_key, get_settings_mask_for_user
from web.models import SettingsResponse, SettingsUpdate
from web.user_store import get_user_secret, set_user_secret

logger = structlog.get_logger()

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("", response_model=SettingsResponse)
async def get_settings(user: dict = Depends(get_current_user)):
    """Return per-user settings with bool mask for secrets."""
    mask = get_settings_mask_for_user(user["id"])
    logger.info(
        "settings.get",
        user_id=user["id"],
        keys_set={k: v for k, v in mask.items() if k.endswith("_set")},
    )
    return SettingsResponse(**mask)


@router.put("", response_model=SettingsResponse)
async def update_settings(
    body: SettingsUpdate,
    user: dict = Depends(get_current_user),
):
    """Encrypt and save per-user settings."""
    fernet_key = get_secret_key()
    update_data = body.model_dump(exclude_none=True)

    for key, value in update_data.items():
        set_user_secret(user["id"], key, str(value), fernet_key)

    logger.info("settings.updated", user_id=user["id"], keys=list(update_data.keys()))
    return SettingsResponse(**get_settings_mask_for_user(user["id"]))


@router.post("/test-llm")
async def test_llm_connectivity(user: dict = Depends(get_current_user)):
    """Test that the stored LLM API key works with a minimal call."""
    fernet_key = get_secret_key()
    api_key = get_user_secret(user["id"], "llm_api_key", fernet_key)
    if not api_key:
        raise HTTPException(status_code=400, detail="No API key configured")

    provider_name = get_user_secret(user["id"], "llm_provider", fernet_key) or "auto"

    try:
        from llm import create_llm_provider

        provider = create_llm_provider(provider=provider_name, api_key=api_key)
        response = provider.generate(
            system="Reply with exactly: ok",
            prompt="ping",
            max_tokens=5,
        )
        return {"ok": True, "provider": provider.provider_name, "response": response.strip()}
    except Exception as e:
        logger.warning("settings.test_llm_failed", user_id=user["id"], error=str(e))
        raise HTTPException(status_code=422, detail=str(e))
