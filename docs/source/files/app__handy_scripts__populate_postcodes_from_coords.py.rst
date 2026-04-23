app/handy_scripts/populate_postcodes_from_coords.py
===================================================

Overview
--------

It iterates rows with coordinates, calls a geocoding service, and persists resolved postcode values. The script is meant for data repair and migration-like operations rather than normal request traffic. It helps keep location search and map features consistent when historical rows lack postcodes.

Purpose
-------

This script backfills missing postcodes by reverse-geocoding existing latitude/longitude records.
