dashboard.css - Barber Dashboard Page Styles
==========================================

**Purpose**: Styling for barber management dashboard.

**What it styles**:

- Dashboard layout with sidebar
- Navigation menu
- Stats/metrics cards
- Profile editing section
- Gallery management
- Schedule editor
- Review section
- Activity feed

**How to use**:

Include in CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/pages/dashboard.css') }}">

**Dashboard Sections**:

- **Sidebar**: Navigation links
- **Header**: User info, notifications
- **Stats**: Views, followers, ratings
- **Profile Tab**: Edit info and photo
- **Gallery Tab**: Manage portfolio
- **Schedule Tab**: Edit working hours
- **Reviews Tab**: View feedback

**Key CSS Classes**:

- ``.dashboard-container``: Main wrapper
- ``.dashboard-sidebar``: Navigation sidebar
- ``.dashboard-content``: Main content area
- ``.dashboard-section``: Individual section
- ``.stats-card``: Metric display
- ``.tab-content``: Tab content area

**Features**:

- Tabbed interface
- Sidebar navigation
- Stats overview
- Form sections
- Save/cancel buttons
- Responsive layout

app/static/css/pages/dashboard.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. Its rules provide the base visual treatment used when rendering the related template/components. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the dashboard page. It styles selectors such as .dashboard-container, .dashboard-header, .dashboard-header h1, and .dashboard-links.
