app/auth.py - Supabase JWT Authentication
===========================================

**Purpose**: Verify and validate JWT tokens from Supabase authentication service.

**What it does**:

This module handles verification of JSON Web Tokens (JWTs) issued by Supabase Auth. It fetches public keys from Supabase and validates token signatures, ensuring that only authenticated users with valid tokens can access protected endpoints.

**Key Functions**:

- ``verify_supabase_jwt(access_token: str)``: Verifies the JWT signature and returns decoded token claims
- ``_get_jwk_client()``: Gets or creates a JWK client for fetching signing keys from Supabase

**How to use**:

In protected routes, call this function to verify user tokens::

    from app.auth import verify_supabase_jwt
    
    try:
        claims = verify_supabase_jwt(user_token)
        user_id = claims['sub']  # Get user ID from token
    except Exception as e:
        # Token is invalid or expired
        return {"error": "Unauthorized"}, 401

**Environment Requirements**:

- ``SUPABASE_URL``: Your Supabase project URL (e.g., https://xxx.supabase.co)

**Token Claims**:

Successfully verified tokens contain:

- ``sub``: Subject (user UUID)
- ``email``: User's email address
- ``aud``: Audience (typically 'authenticated' or 'anon')
- ``exp``: Token expiration timestamp

Overview
--------

It caches a PyJWKClient instance for key discovery and decodes JWTs with issuer and audience validation. API and route handlers call verify_supabase_jwt to trust incoming identity claims. Invalid or malformed tokens raise explicit authentication exceptions.

Purpose
-------

This module in `app/auth.py` provides backend application behavior. Function responsibilities: `_get_jwk_client` retrieves jwk client; `verify_supabase_jwt` verifies supabase JWT.