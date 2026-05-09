base.html - Base HTML Template
==============================

**Purpose**: Master template that all other pages extend from.

**What it contains**:

- HTML document structure and meta tags
- Navigation bar/header
- CSS and JavaScript includes
- Footer
- Jinja2 template blocks for page content
- Session/authentication checks
- CSRF protection tokens

**Key Blocks**:

- ``{% block title %}``: Page title
- ``{% block content %}``: Main page content
- ``{% block scripts %}``: Page-specific JavaScript
- ``{% block extra_css %}``: Page-specific styles

**How to use**:

Extend base template in other pages::

    {% extends "base.html" %}
    
    {% block title %}My Profile{% endblock %}
    
    {% block content %}
        <div class="container">
            <h1>{{ user.username }}'s Profile</h1>
            <!-- Page content -->
        </div>
    {% endblock %}

**Navigation**:

Automatic navbar includes:

- Logo and branding
- Main navigation links
- User menu (login/logout/profile)
- Search bar
- Responsive hamburger menu on mobile

**Layout Structure**::

    <html>
        <head><!-- Meta, CSS, scripts --></head>
        <body>
            <header><!-- Navigation --></header>
            <main>{% block content %}</main>
            <footer><!-- Footer --></footer>
        </body>
    </html>

**Global Variables Available**:

- ``user``: Current logged-in user
- ``is_authenticated``: Boolean login status
- ``user_role``: 'customer' or 'barber'
- ``csrf_token``: For form submissions=

Overview
--------

app/templates/base.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It composes display sections for content rendering and component mounting points used by client scripts. Named template blocks such as title, styles, content, and scripts allow base layout integration and page-specific content injection.

Purpose
-------

This template renders the base view for the web application.
