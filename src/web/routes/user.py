"""User profile (name, email) routes."""

import structlog
from fastapi import APIRouter, Depends

from web.auth import get_current_user
from web.models import UserMe, UserMeUpdate
from web.user_store import get_user_name, update_user_name

logger = structlog.get_logger()

router = APIRouter(prefix="/api/user", tags=["user"])


@router.get("/me", response_model=UserMe)
async def get_me(user: dict = Depends(get_current_user)):
    return UserMe(name=user.get("name"), email=user.get("email"))


@router.patch("/me", response_model=UserMe)
async def update_me(body: UserMeUpdate, user: dict = Depends(get_current_user)):
    if body.name is not None:
        update_user_name(user["id"], body.name.strip())
        logger.info("user.name_updated", user_id=user["id"])
    name = get_user_name(user["id"])
    return UserMe(name=name, email=user.get("email"))
