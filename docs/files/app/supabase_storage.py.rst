app/supabase_storage.py - Supabase Cloud Storage
================================================

**Purpose**: Handles file uploads and retrieval from Supabase Storage (cloud storage service).

**What it does**:

This module manages all image and media file operations:

- Uploads profile photos to cloud storage
- Uploads haircut/gallery photos
- Generates signed URLs for secure access to private files
- Handles storage path management

**Key Functions**:

- ``upload_photo_to_storage(bucket, file_path, file_bytes, content_type)``: Uploads a file to Supabase Storage
- ``sign_storage_path(bucket, path)``: Generates a temporary signed URL for accessing a private file

**How to use**:

Upload and retrieve images::

    from app.supabase_storage import upload_photo_to_storage, sign_storage_path
    
    # Upload a photo
    upload_photo_to_storage(
        bucket='photos',
        file_path='users/123/profile.jpg',
        file_bytes=image_data,
        content_type='image/jpeg'
    )
    
    # Get a temporary access link
    signed_url = sign_storage_path('photos', 'users/123/profile.jpg')

**Storage Buckets**:

- ``profile-photos``: User profile pictures
- ``gallery-photos``: Haircut gallery photos
- ``shop-photos``: Barbershop photos

**Environment Requirements**:

- ``SUPABASE_URL``: Supabase project URL
- ``SUPABASE_KEY``: Supabase API key

**Security Features**:

- Signed URLs expire after a set time period
- Private files require valid signature to access
- Files are served over HTTPS
- Prevents direct public access to sensitive images=

Overview
--------

It initializes the Supabase client, uploads binary image payloads, and creates time-limited signed URLs for secure access. API and route handlers call these functions when saving photo content or returning display-ready image links. Storage path construction keeps uploaded files grouped by barber identity.

Purpose
-------

This module in `app/supabase_storage.py` provides backend application behavior. Function responsibilities: `get_supabase` returns a configured Supabase client instance; `sign_storage_path` signs a storage path (for example `barber_12/photo_987.jpg`) and returns a temporary public URL; `upload_photo_to_storage` uploads image bytes to Supabase Storage and returns the saved storage path.
