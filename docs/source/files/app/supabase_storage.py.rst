app/supabase_storage.py
=======================

Overview
--------

It initializes the Supabase client, uploads binary image payloads, and creates time-limited signed URLs for secure access. API and route handlers call these functions when saving photo content or returning display-ready image links. Storage path construction keeps uploaded files grouped by barber identity.

Purpose
-------

This module in `app/supabase_storage.py` provides backend application behavior. Function responsibilities: `get_supabase` returns a configured Supabase client instance; `sign_storage_path` signs a storage path (for example `barber_12/photo_987.jpg`) and returns a temporary public URL; `upload_photo_to_storage` uploads image bytes to Supabase Storage and returns the saved storage path.
