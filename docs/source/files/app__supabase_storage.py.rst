app/supabase_storage.py
=======================

Overview
--------

It initializes the Supabase client, uploads binary image payloads, and creates time-limited signed URLs for secure access. API and route handlers call these functions when saving photo content or returning display-ready image links. Storage path construction keeps uploaded files grouped by barber identity.

Purpose
-------

This module in `app/supabase_storage.py` provides backend application behavior. Function responsibilities: `get_supabase` retrieves supabase; `sign_storage_path` given a storage path like 'barber_12/photo_987.jpg', returns a signed URL; `upload_photo_to_storage` upload a photo to Supabase storage and return the storage path.