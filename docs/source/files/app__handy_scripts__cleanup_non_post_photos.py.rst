app/handy_scripts/cleanup_non_post_photos.py
============================================

Overview
--------

It connects to the application database and prunes records based on non-post criteria. The script is intended for one-off cleanup operations outside normal request handling. It helps keep gallery/storage data tidy during development or data maintenance tasks.

Purpose
-------

This script in `app/handy_scripts/cleanup_non_post_photos.py` performs maintenance and data operations. Function responsibilities: `cleanup_non_post_photos` deletes all non-post haircutphotos except for the 8 most recent ones.