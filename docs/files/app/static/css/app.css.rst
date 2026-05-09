app/static/css/app.css - Application-Wide Styles
==================================

**Purpose**: Core application-wide CSS rules and utilities.

**What it contains**:

- Base HTML element styles (body, headings, links, text)
- Global layout utilities and responsive grid system
- Common spacing and sizing classes
- Font definitions and typography system
- Color scheme and theme variables
- CSS custom properties (variables) for reusable values

**Key Classes**:

- ``.container``: Responsive content wrapper
- ``.row``, ``.col``: Flex-based grid layout system
- ``.mt-*``, ``.mb-*``, ``.p-*``: Margin and padding utilities
- ``.text-*``: Text color utilities
- ``.bg-*``: Background color utilities
- ``.btn``: Base button styles

**How to use**:

Include in HTML base template::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">

Use utility classes in HTML::

    <div class="container mt-3 mb-4">
        <h1 class="text-primary">Welcome</h1>
    </div>

**Responsive Breakpoints**:

- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

**Color Scheme**:

Defined as CSS variables in ``:root``:

- ``--primary-color``: Main brand color
- ``--secondary-color``: Accent color
- ``--text-color``: Main text
- ``--bg-color``: Page background===============

Overview
--------

app/static/css/app.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. It includes 2 media query block(s) to adapt the interface across viewport sizes. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for shared application UI. It styles selectors such as .container, .nav, .nav-inner, and .brand.
