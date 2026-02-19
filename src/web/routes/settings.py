"""API key and settings management routes."""

from fastapi import APIRouter, Depends

from web.auth import get_current_user
from web.crypto import save_secrets
from web.deps import get_secret_key, get_settings_mask, load_secrets
from web.models import SettingsResponse, SettingsUpdate

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("", response_model=SettingsResponse)
async def get_settings(user: dict = Depends(get_current_user)):
    """Return settings with bool mask for secrets. Never returns raw keys."""
    return SettingsResponse(**get_settings_mask())


@router.put("", response_model=SettingsResponse)
async def update_settings(
    body: SettingsUpdate,
    user: dict = Depends(get_current_user),
):
    """Encrypt and save settings. Only updates fields that are provided."""
    secret_key = get_secret_key()
    secrets = load_secrets(secret_key)

    update_data = body.model_dump(exclude_none=True)
    secrets.update(update_data)

    save_secrets(secret_key, secrets)

    return SettingsResponse(**get_settings_mask())
