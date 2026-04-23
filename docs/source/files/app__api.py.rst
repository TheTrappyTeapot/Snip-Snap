app/api.py
==========

Overview
--------

It validates request payloads, reads the authenticated session user, and coordinates with the db and storage layers. Gallery/photo responses include signed storage URLs so private assets can be rendered safely in the frontend. Cursor helpers support discover feed pagination and stable ordering between API calls.

Purpose
-------

This module in `app/api.py` provides backend application behavior. Function responsibilities: `create_user` create a new App_User record for signup; `barbershops` returns barbershop data for the map endpoint; `save_user_location` saves user location; `discover_search_items` returns discover search items for frontend filters; `_parse_cursor` parses pagination cursor; `_make_next_cursor` items from fetch_discover_posts are RealDictCursor dicts containing created_at + photo_id; `gallery_posts` returns filtered discover gallery posts with pagination data; `update_profile` update user profile (username, location, role, latitude, longitude, and barbershop for barbers); `get_barbershops` get all barbershops for autocomplete in profile; `get_current_barbershop` get the current barber's barbershop; `create_new_barbershop` create a new barbershop and optionally assign it to the current barber; `upload_profile_photo` upload a profile photo for the current user; `upload_photo` upload a photo post.