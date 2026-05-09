app/handy_scripts/clear_all_photos.py - Delete All Photos
========================================

**Purpose**: Utility script to completely clear all photos from the storage system.

**What it does**:

This maintenance script:

- Deletes all user photos from Supabase storage
- Clears profile photos and gallery photos
- Removes all uploaded images
- Resets storage to empty state

**How to use**:

Run from the command line::

    python -m app.handy_scripts.clear_all_photos

**When to use**:

- Development/testing: Reset database to clean state
- Migration: Move to new storage provider
- Data cleanup: Remove sensitive user data

**⚠️ WARNING - DESTRUCTIVE ⚠️**:

This script:

- **Permanently deletes ALL photos** - cannot be undone
- Removes user profile pictures
- Removes all haircut gallery photos
- Removes barbershop images

Only run if you're certain you want to delete everything!

**Safe Alternative**:

For production, consider:

- Using manual Supabase dashboard deletion
- Creating database backups first
- Testing in development environment first==================

Overview
--------

It performs bulk deletion logic against photo-related tables in the app database. Developers run it when they need a clean state before reseeding or validating gallery features. The script is intentionally separate from runtime app code to avoid accidental route exposure.

Purpose
-------

This script in `app/handy_scripts/clear_all_photos.py` performs maintenance and data operations. Function responsibilities: `clear_all_photos` deletes all records from haircutphoto_tag and haircutphoto.