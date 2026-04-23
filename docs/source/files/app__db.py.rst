app/db.py
=========

Overview
--------

It opens PostgreSQL connections and implements query helpers used by route handlers and JSON APIs throughout the app. The module includes profile updates, gallery/photo writes, discover feed retrieval, map/search data queries, and review persistence. Most web endpoints delegate persistence work to these functions to keep request handlers thin.

Purpose
-------

This module is the primary data-access layer for users, barbers, barbershops, photos, search, and reviews.
