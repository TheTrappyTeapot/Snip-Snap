app/access.py
=============

Overview
--------

It resolves the current user role from the session and provides login_required and roles_required wrappers. Route handlers use these decorators to enforce authentication and role checks before executing business logic. Failed checks return redirects or HTTP errors instead of route content.

Purpose
-------

This module centralizes session-based access control decorators for protected routes.
