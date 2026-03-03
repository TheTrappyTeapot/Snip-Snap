# app/services/auth_service.py
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from flask import Request

from app.db.queries import (
    get_app_user_by_auth_user_id,
    set_auth_user_id_for_user,
)

try:
    import jwt  # PyJWT
except ImportError as e:  # pragma: no cover
    raise RuntimeError(
        "Missing dependency: PyJWT. Install with: pip install PyJWT"
    ) from e


@dataclass(frozen=True)
class CurrentUser:
    auth_user_id: str  # Supabase Auth UUID (string)
    user_id: int       # Internal App_User.user_id (int)
    role: str          # 'customer' | 'barber' | etc.


def _get_bearer_token(req: Request) -> Optional[str]:
    auth = req.headers.get("Authorization", "")
    if not auth:
        return None
    parts = auth.split(" ", 1)
    if len(parts) != 2:
        return None
    scheme, token = parts[0].strip(), parts[1].strip()
    if scheme.lower() != "bearer" or not token:
        return None
    return token


def _verify_supabase_jwt(token: str) -> str:
    secret = os.environ.get("SUPABASE_JWT_SECRET")
    if not secret:
        raise RuntimeError("SUPABASE_JWT_SECRET environment variable is not set")

    # Supabase defaults to aud="authenticated", but allow disabling if needed
    audience = os.environ.get("SUPABASE_JWT_AUDIENCE", "authenticated")
    verify_aud = os.environ.get("SUPABASE_VERIFY_AUDIENCE", "true").lower() in ("1", "true", "yes")

    options = {"verify_aud": verify_aud}

    payload = jwt.decode(
        token,
        secret,
        algorithms=["HS256"],
        audience=audience if verify_aud else None,
        options=options,
    )

    auth_user_id = payload.get("sub")
    if not isinstance(auth_user_id, str) or not auth_user_id.strip():
        raise ValueError("JWT is missing 'sub' claim (auth user id)")

    return auth_user_id.strip()


def try_get_current_user(req: Request) -> Optional[CurrentUser]:
    """
    Returns CurrentUser if an Authorization Bearer token is present and valid.
    Returns None if no token is present.
    Raises ValueError for invalid tokens.
    """
    token = _get_bearer_token(req)
    if not token:
        return None

    auth_user_id = _verify_supabase_jwt(token)

    row = get_app_user_by_auth_user_id(auth_user_id)
    if row is None:
        # Auth is valid but not mapped to an App_User yet.
        # Caller can decide to onboard/register; for now return None.
        return None

    return CurrentUser(
        auth_user_id=auth_user_id,
        user_id=int(row["user_id"]),
        role=str(row.get("role") or ""),
    )


def require_current_user(req: Request) -> CurrentUser:
    """
    Returns CurrentUser or raises ValueError if unauthenticated/unknown.
    """
    user = try_get_current_user(req)
    if user is None:
        raise ValueError("Unauthenticated or unknown user")
    return user


def link_auth_user_to_existing_app_user(user_id: int, auth_user_id: str) -> None:
    """
    Utility for onboarding flows: link an existing App_User row to a Supabase auth user id.
    """
    set_auth_user_id_for_user(user_id=user_id, auth_user_id=auth_user_id)