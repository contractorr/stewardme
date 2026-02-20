"""JWT validation middleware for FastAPI."""

import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from web.user_store import get_or_create_user

ALGORITHM = "HS256"

security = HTTPBearer()


def _get_jwt_secret() -> str:
    secret = os.getenv("NEXTAUTH_SECRET")
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="NEXTAUTH_SECRET not configured",
        )
    return secret


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Decode JWT, extract user info, auto-register on first login."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, _get_jwt_secret(), algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing sub",
            )
        # Upsert user in DB on every auth
        get_or_create_user(user_id, email=payload.get("email"), name=payload.get("name"))
        return {
            "id": user_id,
            "email": payload.get("email"),
            "name": payload.get("name"),
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
