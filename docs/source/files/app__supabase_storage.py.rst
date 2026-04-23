app/supabase_storage.py
=======================

Overview
--------

It initializes the Supabase client, uploads binary image payloads, and creates time-limited signed URLs for secure access. API and route handlers call these functions when saving photo content or returning display-ready image links. Storage path construction keeps uploaded files grouped by barber identity.

Purpose
-------

This module wraps Supabase Storage operations used by profile and gallery uploads.
