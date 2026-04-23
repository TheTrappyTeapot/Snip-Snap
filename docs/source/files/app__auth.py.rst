app/auth.py
===========

Overview
--------

It caches a PyJWKClient instance for key discovery and decodes JWTs with issuer and audience validation. API and route handlers call verify_supabase_jwt to trust incoming identity claims. Invalid or malformed tokens raise explicit authentication exceptions.

Purpose
-------

This module in `app/auth.py` provides backend application behavior. Function responsibilities: `_get_jwk_client` retrieves jwk client; `verify_supabase_jwt` verifies supabase JWT.