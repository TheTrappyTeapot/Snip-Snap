app/access.py
=============

Overview
--------

It resolves the current user role from the session and provides login_required and roles_required wrappers. Route handlers use these decorators to enforce authentication and role checks before executing business logic. Failed checks return redirects or HTTP errors instead of route content.

Purpose
-------

This module in `app/access.py` provides backend application behavior. Function responsibilities: `current_role` returns the logged-in user role from session data; `login_required` wraps route handlers to require an authenticated user; `roles_required` builds decorators that enforce allowed user roles.