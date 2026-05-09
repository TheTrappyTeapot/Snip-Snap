mapWidget.css - Interactive Map Component Styles
================================================

**Purpose**: Styles for the interactive map widget showing barbershop locations.

**What it styles**:

- Map container and sizing
- Map markers and location pins
- Popup/info windows for shop details
- Map controls (zoom, pan, etc.)
- Responsive map behavior
- Location filtering sidebar

**How to use**:

Include CSS and map library (Leaflet/Google Maps)::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/mapWidget.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/leaflet"></script>

HTML structure::

    <div class="map-container">
        <div class="map" id="mapElement"></div>
        <div class="map-sidebar">
            <!-- Location list -->
        </div>
    </div>

**Key CSS Classes**:

- ``.map-container``: Main wrapper
- ``.map``: Map canvas element
- ``.map-marker``: Location pin style
- ``.map-popup``: Info window/bubble
- ``.map-sidebar``: Shop list sidebar
- ``.map-control``: Zoom/control buttons

**Features**:

- Clickable markers for shop details
- Popup shows barber/shop information
- List view sidebar with clickable items
- Responsive: sidebar collapses on mobile
- Dark/light theme support

**Interactions**:

- Click marker to show popup
- Click list item to center map
- Zoom and pan controls
- Mobile: touch gestures for navigation

app/static/css/components/mapWidget.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. Its rules provide the base visual treatment used when rendering the related template/components. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the mapWidget component. It styles selectors such as .map-widget-wrapper, .map-widget-map, .map-widget-overlay, and .map-widget-overlay span.
