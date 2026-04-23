app/routes.py
=============

Overview
--------

It renders Jinja templates for public and authenticated pages, handles auth redirects, and exposes helper endpoints used by frontend widgets. Route handlers combine session checks with database helper calls to populate profile, gallery, map, and review screens. It also includes convenience logic such as closing-soon calculations and media update endpoints.

Purpose
-------

This module in `app/routes.py` provides backend application behavior. Function responsibilities: `get_closing_soon_info` check if a closing time is within the next 2 hours; `get_current_day_num` get current day of week (0=Monday, 6=Sunday); `register_routes` register API endpoints and page routes on the Flask app.