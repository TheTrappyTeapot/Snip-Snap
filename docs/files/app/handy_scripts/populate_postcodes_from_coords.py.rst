app/handy_scripts/populate_postcodes_from_coords.py - Geocoding Utility
======================================================

**Purpose**: Utility script to populate UK postcodes based on geographic coordinates (latitude/longitude).

**What it does**:

This utility:

- Takes stored latitude/longitude coordinates
- Uses reverse geocoding to find corresponding UK postcodes
- Updates the database with postcode information
- Enables postcode-based search functionality
- Improves location accuracy for barbershops

**How to use**:

Run from the command line::

    python -m app.handy_scripts.populate_postcodes_from_coords

**When to use**:

- Initial data import: When adding barbershops with GPS coordinates
- Migration: Converting from coordinate-only to coordinate+postcode
- Data enrichment: Adding missing postcode data
- Maintenance: Ensuring all locations have postcodes

**Requirements**:

- Valid latitude/longitude coordinates in database
- Geocoding API access (Google Maps, OpenStreetMap, etc.)
- API credentials configured in environment

**Output**:

Script will report:

- Number of locations processed
- Postcodes successfully matched
- Any locations with matching failures
- Processing time and status

**Environment Variables Needed**::

    GEOCODING_API_KEY=your_api_key
    GEOCODING_SERVICE=google  # or 'openstreetmap'===================

Overview
--------

It iterates rows with coordinates, calls a geocoding service, and persists resolved postcode values. The script is meant for data repair and migration-like operations rather than normal request traffic. It helps keep location search and map features consistent when historical rows lack postcodes.

Purpose
-------

This script in `app/handy_scripts/populate_postcodes_from_coords.py` performs maintenance and data operations. Function responsibilities: `reverse_geocode` convert latitude/longitude to postcode using postcodes.io API; `populate_postcodes` fetch all users with location_lat/location_lng but no postcode, reverse geocode their coordinates, and update their postcode in DB.