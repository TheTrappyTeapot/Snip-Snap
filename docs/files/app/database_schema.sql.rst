app/database_schema.sql - Database Schema Definition
=================================================

**Purpose**: Defines the PostgreSQL database structure and tables for the Snip-Snap application.

**What it contains**:

SQL DDL (Data Definition Language) statements that create all database tables including:

- **App_User**: Core user information (customers and barbers)
- **Barber**: Extended barber profile information
- **Barbershop**: Barbershop location and details
- **Gallery_Photos**: Photo posts from barbers
- **Reviews**: Customer reviews of barbers
- **Social**: Follow relationships between users
- Indexes for performance optimization

**Key Tables**:

- ``App_User``: user_id, email, username, role, auth_user_id, location
- ``Barber``: barber_id, user_id, bio, barbershop_id, social_links
- ``Barbershop``: barbershop_id, name, location, latitude, longitude, website
- ``Gallery_Photos``: photo_id, user_id, storage_path, created_at
- ``Reviews``: review_id, barber_id, customer_id, rating, text, created_at

**How to use**:

The database is initialized from Supabase. To view or modify the schema:

1. Go to Supabase Dashboard
2. Navigate to SQL Editor
3. Execute queries to view or modify schema
4. Use this file as reference documentation

**Important Notes**:

- All user IDs reference Supabase Auth UUIDs
- Timestamps use UTC timezone
- Locations stored as POINT (latitude, longitude) for geographic queries
- Indexes on frequently queried columns for performance
- Foreign key constraints maintain referential integrity===

Overview
--------

app/database_schema.sql creates core tables, foreign keys, and indexes that support users, barbers, shops, photos, tags, and reviews. Notable table definitions include public, public, public, public, public, and public. Application database helper functions in app/db.py assume this schema when executing reads and writes for API and route handlers.

Purpose
-------

This SQL file defines the relational schema and constraints used by the Snip-Snap backend.
