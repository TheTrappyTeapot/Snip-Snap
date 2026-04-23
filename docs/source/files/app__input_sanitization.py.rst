app/input_sanitization.py
=========================

Overview
--------

It normalizes and cleans input to reduce malformed values before database writes and template rendering. Route and API handlers call sanitize_input when accepting profile and review content. Keeping sanitization in one helper avoids inconsistent validation behavior across endpoints.

Purpose
-------

This module in `app/input_sanitization.py` provides backend application behavior. Function responsibilities: `sanitize_input` validate a user-supplied string.