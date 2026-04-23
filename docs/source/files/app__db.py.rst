app/db.py
=========

Overview
--------

It opens PostgreSQL connections and implements query helpers used by route handlers and JSON APIs throughout the app. The module includes profile updates, gallery/photo writes, discover feed retrieval, map/search data queries, and review persistence. Most web endpoints delegate persistence work to these functions to keep request handlers thin.

Purpose
-------

This module in `app/db.py` provides backend application behavior. Function responsibilities are grouped by feature area:

- **Connection and auth-user linking:** `_get_conn` opens the PostgreSQL connection; `create_app_user` inserts a new `App_User`; `link_auth_user_id` links a Supabase auth UUID to an app user; `get_app_user_by_auth_user_id` and `get_app_user_by_email` retrieve app-user records by auth UUID or email.
- **User/profile reads and writes:** `get_user_promo` returns data for the user promo component; `update_user_profile` saves username/postcode/role and optional coordinates; `update_user_location` and `get_user_location` manage stored coordinates; `update_user_postcode` and `get_user_postcode` manage stored postcodes.
- **Barber and barbershop data:** `get_barber_public_by_user_id`, `get_barber_id_from_user_id`, `get_barbershop_by_id`, `get_barber_barbershop`, and `get_all_barbershops` fetch barber/barbershop records; `create_or_update_barber`, `update_barber_barbershop`, and `create_barbershop` create or update barber/shop links and shop entries.
- **Barber profile and timetable editing:** `update_barber_profile`, `update_barber_bio`, `update_barbershop_website`, and `update_barber_social_links` update barber-facing profile fields; `get_shifts_for_barber`, `add_shift`, `delete_shift`, and `get_shop_opening_hours` manage shifts and derive aggregate opening hours.
- **Photos, tags, and discover feed:** `filter_existing_tag_ids` validates tag IDs; `create_haircut_post` inserts post photos; `fetch_discover_posts` and `fetch_discover_search_items` return discover data; `_pick_label` maps filter labels; `get_barbershops_for_map` returns map-ready barbershop/barber data.
- **Reviews and location lookup:** `get_reviews_for_barber` retrieves barber reviews; `submit_barber_review` inserts a review row; `postcode_to_coordinates` converts UK postcodes to coordinates via postcodes.io.
- **Profile/gallery image records:** `update_or_create_profile_photo` and `get_profile_photo` manage profile photo metadata; `get_barber_gallery_photos` and `get_barbershop_gallery_photos` return non-post gallery photos for barber and shop views.
