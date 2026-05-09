app/routes.py - Page Routing and View Handlers
==============================================

**Purpose**: Flask routes that render HTML pages and handle server-side page logic.

**What it does**:

This module defines all URL routes and their corresponding view functions. It handles:

- Page rendering (login, signup, profile, dashboard, etc.)
- User authentication flow (login, logout, signup)
- Page data loading (barbershop info, user profiles, gallery posts)
- Form submission handling
- Redirect logic for authenticated pages

**Key Routes**:

- ``/login``: User login page
- ``/signup``: User registration page
- ``/profile``: User profile page (login_required)
- ``/dashboard``: Barber dashboard (roles_required: barber)
- ``/barbershop/<id>``: Barbershop profile page
- ``/barber/<id>``: Barber profile page
- ``/discover``: Gallery discovery page
- ``/map``: Interactive map of barbershops

**Helper Functions**:

- ``get_closing_soon_info()``: Checks if a barbershop is closing within 2 hours
- ``get_current_day_num()``: Gets current day number (0-6 for week navigation)

**How to use**:

Routes are automatically registered on app startup::

    from app.routes import register_routes
    register_routes(app)  # Registers all routes in app

Users navigate to URLs like ``/profile`` to access these pages.

**Key Features**:

- Protected routes require authentication (via @login_required)
- Barber-only routes require barber role (via @roles_required('barber'))
- Automatic redirect to login for unauthorized access
- Dynamic page data loaded from database

Overview
--------

It renders Jinja templates for public and authenticated pages, handles auth redirects, and exposes helper endpoints used by frontend widgets. Route handlers combine session checks with database helper calls to populate profile, gallery, map, and review screens. It also includes convenience logic such as closing-soon calculations and media update endpoints.

Purpose
-------

This module in `app/routes.py` provides backend application behavior. Function responsibilities: `get_closing_soon_info` check if a closing time is within the next 2 hours; `get_current_day_num` get current day of week (0=Monday, 6=Sunday); `register_routes` register API endpoints and page routes on the Flask app.