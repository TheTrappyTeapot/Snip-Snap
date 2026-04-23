app/handy_scripts/clear_all_photos.py
=====================================

Overview
--------

It performs bulk deletion logic against photo-related tables in the app database. Developers run it when they need a clean state before reseeding or validating gallery features. The script is intentionally separate from runtime app code to avoid accidental route exposure.

Purpose
-------

This maintenance script clears haircut photo records for reset or test data workflows.
