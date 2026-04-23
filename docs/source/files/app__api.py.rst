app/api.py
==========

Overview
--------

It validates request payloads, reads the authenticated session user, and coordinates with the db and storage layers. Gallery/photo responses include signed storage URLs so private assets can be rendered safely in the frontend. Cursor helpers support discover feed pagination and stable ordering between API calls.

Purpose
-------

This module defines Flask API endpoints for signup profile creation, discovery feed data, map data, profile updates, and media uploads.
