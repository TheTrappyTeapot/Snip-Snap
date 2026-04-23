app/handy_scripts/generate_haircut_photos.py
============================================

Overview
--------

It samples storage images, chooses randomized timestamps/statuses/tags, and inserts rows associated with barbers. The generation flow uses helper functions for dimensions, tag sets, and photo metadata so output is varied but structured. It is used offline to quickly populate discover/gallery views with representative content.

Purpose
-------

This script in `app/handy_scripts/generate_haircut_photos.py` performs maintenance and data operations. Function responsibilities: `get_storage_image_pool` loads usable `photos/haircuts` storage paths from Supabase; `random_timestamp` generates a timestamp within the configured recent-day window; `choose_status` picks a visible/hidden status using the hidden-ratio probability; `choose_dimensions` selects one of the predefined social-image dimensions; `choose_tags` samples a non-duplicated set of tag IDs for a generated photo; `main` inserts generated haircutphoto and haircutphoto_tag rows for each barber in a single database transaction.
