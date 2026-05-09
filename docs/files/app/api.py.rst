app/api.py - REST API Endpoints
==============================

**Purpose**: Provides JSON REST API endpoints for frontend applications.

**What it does**:

This module defines all API endpoints used by the frontend (JavaScript) to communicate with the backend. It handles:

- User authentication and registration
- User profile management
- Barbershop and barber data retrieval
- Gallery photo uploads and retrieval
- Review submission and management
- Social features (follow/unfollow)
- Map data for barbershop locations
- Discovery feed with pagination

**Key Endpoints**:

- ``POST /api/auth/create-user``: Create new user account
- ``GET /api/discover``: Get paginated gallery posts
- ``POST /api/upload-photo``: Upload a new gallery photo
- ``PUT /api/profile``: Update user profile
- ``GET /api/barbershops``: Get list of barbershops
- ``POST /api/reviews``: Create a review
- ``GET /api/reviews/<barber_id>``: Get reviews for a barber
- ``POST /api/follow``: Follow a barber
- ``DELETE /api/follow``: Unfollow a barber

**How to use**:

Frontend JavaScript makes requests to these endpoints::

    // JavaScript example
    const response = await fetch('/api/discover?limit=20&offset=0');
    const posts = await response.json();

**Response Format**:

All endpoints return JSON with status information::

    {
        "success": true,
        "data": { ... },
        "message": "Operation successful"
    }

**Authentication**:

Most endpoints require a valid Supabase JWT token in the Authorization header::

    Authorization: Bearer <JWT_TOKEN>

**Error Handling**:

API returns appropriate HTTP status codes:

- ``200``: Success
- ``400``: Bad request (validation error)
- ``401``: Unauthorized (invalid token)
- ``403``: Forbidden (insufficient permissions)
- ``500``: Server error=

Overview
--------

It validates request payloads, reads the authenticated session user, and coordinates with the db and storage layers. Gallery/photo responses include signed storage URLs so private assets can be rendered safely in the frontend. Cursor helpers support discover feed pagination and stable ordering between API calls.

Purpose
-------

This module in `app/api.py` provides backend application behavior. Function responsibilities: `create_user` create a new App_User record for signup; `barbershops` returns barbershop data for the map endpoint; `save_user_location` saves user location; `discover_search_items` returns discover search items for frontend filters; `_parse_cursor` parses pagination cursor; `_make_next_cursor` items from fetch_discover_posts are RealDictCursor dicts containing created_at + photo_id; `gallery_posts` returns filtered discover gallery posts with pagination data; `update_profile` update user profile (username, location, role, latitude, longitude, and barbershop for barbers); `get_barbershops` get all barbershops for autocomplete in profile; `get_current_barbershop` get the current barber's barbershop; `create_new_barbershop` create a new barbershop and optionally assign it to the current barber; `upload_profile_photo` upload a profile photo for the current user; `upload_photo` upload a photo post.