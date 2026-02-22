"""API key and settings management routes (per-user)."""

import structlog
from fastapi import APIRouter, Depends

from web.auth import get_current_user
from web.deps import get_secret_key, get_settings_mask_for_user
from web.models import SettingsResponse, SettingsUpdate
from web.user_store import set_user_secret

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
