app/handy_scripts/generate_haircut_photos.py - Generate Test Photos
==================================================

**Purpose**: Utility script to generate sample haircut photos for testing and development.

**What it does**:

This development script:

- Creates synthetic haircut images using image generation
- Uploads them to the gallery for testing
- Associates photos with test barber accounts
- Generates realistic-looking test data
- Populates the discovery feed for UI testing

**How to use**:

Run from the command line::

    python -m app.handy_scripts.generate_haircut_photos

**When to use**:

- Development: Populate test database with sample data
- UI/UX testing: Test gallery layout with multiple images
- Demo: Show working application to stakeholders
- Load testing: Generate large amounts of test content

**Configuration**:

You can customize:

- Number of photos to generate (default: 20)
- Which barbers to associate photos with
- Photo categories/styles

**Example**::

    # Generate 50 photos for barber_id 1
    python -m app.handy_scripts.generate_haircut_photos --count 50 --barber 1===================

Overview
--------

It samples storage images, chooses randomized timestamps/statuses/tags, and inserts rows associated with barbers. The generation flow uses helper functions for dimensions, tag sets, and photo metadata so output is varied but structured. It is used offline to quickly populate discover/gallery views with representative content.

Purpose
-------

This script in `app/handy_scripts/generate_haircut_photos.py` performs maintenance and data operations. Function responsibilities: `get_storage_image_pool` loads usable `photos/haircuts` storage paths from Supabase; `random_timestamp` generates a timestamp within the configured recent-day window; `choose_status` picks a visible/hidden status using the hidden-ratio probability; `choose_dimensions` selects one of the predefined social-image dimensions; `choose_tags` samples a non-duplicated set of tag IDs for a generated photo; `main` inserts generated haircutphoto and haircutphoto_tag rows for each barber in a single database transaction.
