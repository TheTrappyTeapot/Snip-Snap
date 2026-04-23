app/handy_scripts/generate_haircut_photos.py
============================================

Overview
--------

It samples storage images, chooses randomized timestamps/statuses/tags, and inserts rows associated with barbers. The generation flow uses helper functions for dimensions, tag sets, and photo metadata so output is varied but structured. It is used offline to quickly populate discover/gallery views with representative content.

Purpose
-------

This script in `app/handy_scripts/generate_haircut_photos.py` performs maintenance and data operations. Function responsibilities: `get_storage_image_pool` retrieves storage image pool; `random_timestamp` returns random timestamp; `choose_status` chooses status; `choose_dimensions` chooses dimensions; `choose_tags` chooses tags; `main` returns main.