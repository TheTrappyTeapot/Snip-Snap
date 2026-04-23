app/routes.py
=============

Overview
--------

It renders Jinja templates for public and authenticated pages, handles auth redirects, and exposes helper endpoints used by frontend widgets. Route handlers combine session checks with database helper calls to populate profile, gallery, map, and review screens. It also includes convenience logic such as closing-soon calculations and media update endpoints.

Purpose
-------

This module registers page routes and non-blueprint API routes for the web application.
