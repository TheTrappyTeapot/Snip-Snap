app/handy_scripts/populate_postcodes_from_coords.py
===================================================

Overview
--------

It iterates rows with coordinates, calls a geocoding service, and persists resolved postcode values. The script is meant for data repair and migration-like operations rather than normal request traffic. It helps keep location search and map features consistent when historical rows lack postcodes.

Purpose
-------

This script in `app/handy_scripts/populate_postcodes_from_coords.py` performs maintenance and data operations. Function responsibilities: `reverse_geocode` convert latitude/longitude to postcode using postcodes.io API; `populate_postcodes` fetch all users with location_lat/location_lng but no postcode, reverse geocode their coordinates, and update their postcode in DB.