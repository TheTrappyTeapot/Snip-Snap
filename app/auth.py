"""Module for app/auth.py."""

import os
import jwt
from jwt import PyJWKClient

_JWK_CLIENT = None
_JWK_URL = None


def _get_jwk_client() -> PyJWKClient:
    """Handles get jwk client."""
    global _JWK_CLIENT, _JWK_URL

    supabase_url = os.environ["SUPABASE_URL"].rstrip("/")
    jwk_url = f"{supabase_url}/auth/v1/.well-known/jwks.json"

    if _JWK_CLIENT is None or _JWK_URL != jwk_url:
        _JWK_CLIENT = PyJWKClient(jwk_url)
        _JWK_URL = jwk_url

    return _JWK_CLIENT


def verify_supabase_jwt(access_token: str) -> dict:
    """Handles verify supabase jwt."""
    supabase_url = os.environ["SUPABASE_URL"].rstrip("/")
    issuer = f"{supabase_url}/auth/v1"

    header = jwt.get_unverified_header(access_token)
    print("JWT header:", header)

    # Peek claims without verifying signature, just to inspect aud
    peek = jwt.decode(access_token, options={"verify_signature": False})
    print("JWT aud (peek):", peek.get("aud"), "iss:", peek.get("iss"))

    jwk_client = _get_jwk_client()
    signing_key = jwk_client.get_signing_key_from_jwt(access_token)

    allowed_algs = ["ES256", "RS256", "EdDSA"]

    # Accept common Supabase audiences. Adjust if peek shows something else.
    allowed_audiences = ["authenticated", "anon"]
    print("Allowed audiences:", allowed_audiences)

    claims = jwt.decode(
        access_token,
        signing_key.key,
        algorithms=allowed_algs,
        issuer=issuer,
        audience=allowed_audiences,
        options={"require": ["exp", "iss", "aud"]},
    )
    return claims
