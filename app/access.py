"""Module for app/access.py."""

from __future__ import annotations

from functools import wraps
from typing import Callable, Iterable

from flask import session, redirect, url_for, abort


def current_role() -> str | None:
    """Handles current role."""
    user = session.get("user") or {}
    return user.get("role")


def login_required(view: Callable):
    """Handles login required."""
    @wraps(view)
    def wrapper(*args, **kwargs):
        """Handles wrapper."""
        if not session.get("user"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapper


def roles_required(*allowed_roles: str):
    """Handles roles required."""
    allowed = set(allowed_roles)

    def decorator(view: Callable):
        """Handles decorator."""
        @wraps(view)
        def wrapper(*args, **kwargs):
            """Handles wrapper."""
            user = session.get("user")
            if not user:
                return redirect(url_for("login"))

            role = user.get("role")
            if role not in allowed:
                # If logged in but not permitted
                return abort(403)

            return view(*args, **kwargs)
        return wrapper
    return decorator
