import os
from supabase import create_client

_supabase = None

def get_supabase():
    global _supabase
    if _supabase is None:
        url = os.environ["SUPABASE_URL"]
        key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
        _supabase = create_client(url, key)
    return _supabase

def sign_storage_path(path: str, expires_in: int = 3600) -> str | None:
    """
    Given a storage path like 'barber_12/photo_987.jpg', returns a signed URL.
    """
    bucket = os.environ.get("SUPABASE_STORAGE_BUCKET", "haircuts")
    if not path:
        return None

    sb = get_supabase()
    res = sb.storage.from_(bucket).create_signed_url(path, expires_in)

    # supabase-py returns a dict-like object; support both shapes
    if isinstance(res, dict):
        return res.get("signedURL") or res.get("signedUrl") or res.get("signed_url")
    return getattr(res, "signed_url", None) or getattr(res, "signedURL", None)

def upload_photo_to_storage(barber_id: int, file_data: bytes, filename: str) -> str | None:
    """
    Upload a photo to Supabase storage and return the storage path.
    
    Args:
        barber_id: The barber's ID
        file_data: The file content as bytes
        filename: Original filename (used to get extension)
    
    Returns:
        Storage path (e.g., 'barber_12/photo_123.jpg') or None if upload fails
    """
    bucket = os.environ.get("SUPABASE_STORAGE_BUCKET", "haircuts")
    if not file_data:
        return None
    
    # Generate storage path: barber_<id>/<uuid>.<ext>
    import uuid
    file_ext = os.path.splitext(filename)[1].lower()
    storage_filename = f"{uuid.uuid4()}{file_ext}"
    storage_path = f"barber_{barber_id}/{storage_filename}"
    
    try:
        sb = get_supabase()
        res = sb.storage.from_(bucket).upload(storage_path, file_data)
        # Return the path if upload was successful
        if res:
            return storage_path
        return None
    except Exception as e:
        print(f"[UPLOAD_PHOTO] Error uploading to Supabase: {e}")
        return None