app/static/css/main.css - Main Layout Styles
=============================

**Purpose**: Primary layout and structural CSS for the main application interface.

**What it contains**:

- Navigation bar styles
- Sidebar/navigation menu styling
- Main content area layout
- Footer styling
- Page background and general layout structure
- Responsive layout adjustments

**Key Sections**:

- **Header/Navigation**: Top navbar with logo and menu
- **Main Content**: Central page content area
- **Sidebar**: Optional navigation sidebar
- **Footer**: Bottom page footer
- **Responsive**: Mobile menu toggle and responsive grid

**How to use**:

Include alongside app.css in base template::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">

Structure HTML with semantic layout::

    <header class="navbar">...</header>
    <main class="main-content">
        <nav class="sidebar">...</nav>
        <div class="content">...</div>
    </main>
    <footer>...</footer>

**Mobile Responsive**:

Automatic layout changes for smaller screens:

- Sidebar collapses/hides on mobile
- Header navigation becomes hamburger menu
- Content expands full width
- Touch-friendly spacing increases===============

Overview
--------

app/static/css/main.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. Its rules provide the base visual treatment used when rendering the related template/components. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for shared application UI. It styles selectors such as .container, .site-header, .nav, and .placeholder.
