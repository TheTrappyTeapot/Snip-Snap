app/access.py - Access Control Decorators
=========================================

**Purpose**: Provides decorators for route access control and authentication checks.

**What it does**:

This module implements role-based access control (RBAC) and authentication middleware. It protects routes by checking user session state and role permissions before allowing access.

**Key Functions**:

- ``current_role()``: Gets the current logged-in user's role from session
- ``login_required``: Decorator that redirects unauthenticated users to login page
- ``roles_required(*allowed_roles)``: Decorator that checks if user has one of the allowed roles

**How to use**:

Apply decorators to Flask routes to protect them::

    from flask import Blueprint
    from app.access import login_required, roles_required
    
    @app.route('/profile')
    @login_required
    def profile():
        """Only logged-in users can access"""
        return render_template('profile.html')
    
    @app.route('/barber-dashboard')
    @roles_required('barber')
    def barber_dashboard():
        """Only barbers can access"""
        return render_template('dashboard.html')

**User Roles**:

- ``customer``: Regular user browsing and booking haircuts
- ``barber``: Professional barber with shop management features
- ``admin``: (optional) Administrative access

**Session Storage**:

User information is stored in Flask session::

    session['user'] = {
        'user_id': 123,
        'email': 'user@example.com',
        'role': 'barber'
    }

Overview
--------

It resolves the current user role from the session and provides login_required and roles_required wrappers. Route handlers use these decorators to enforce authentication and role checks before executing business logic. Failed checks return redirects or HTTP errors instead of route content.

Purpose
-------

This module in `app/access.py` provides backend application behavior. Function responsibilities: `current_role` returns the logged-in user role from session data; `login_required` wraps route handlers to require an authenticated user; `roles_required` builds decorators that enforce allowed user roles.