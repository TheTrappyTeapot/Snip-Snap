app/handy_scripts/cleanup_non_post_photos.py - Remove Non-Post Photos
====================================================

**Purpose**: Utility script to clean up photos from cloud storage that are not associated with any gallery post.

**What it does**:

This maintenance script:

- Scans the Supabase storage for orphaned photos
- Identifies photos that were uploaded but never linked to a post
- Removes these unused files to save storage space
- Frees up Supabase storage quota

**How to use**:

Run from the command line::

    python -m app.handy_scripts.cleanup_non_post_photos

**When to run**:

- After users delete posts with photos
- Periodically for storage maintenance
- When storage quota is running low

**Output**:

Script will display:

- Number of orphaned photos found
- Files being removed
- Total storage space freed
- Any errors encountered

**Warning**:

This is a destructive operation - it permanently deletes files. Ensure backups exist before running.==================

Overview
--------

It connects to the application database and prunes records based on non-post criteria. The script is intended for one-off cleanup operations outside normal request handling. It helps keep gallery/storage data tidy during development or data maintenance tasks.

Purpose
-------

This script in `app/handy_scripts/cleanup_non_post_photos.py` performs maintenance and data operations. Function responsibilities: `cleanup_non_post_photos` deletes all non-post haircutphotos except for the 8 most recent ones.