mapWidget.js - Interactive Map Component Script
===============================================

**Purpose**: JavaScript functionality for the interactive barbershop location map.

**What it does**:

- Initializes the map with Leaflet or Google Maps
- Fetches barbershop locations from the API
- Adds map markers for each location
- Handles marker clicks to show shop details
- Manages map interactions (pan, zoom, search)
- Syncs map with sidebar location list
- Handles filtering by location/services

**How to use**:

Include in HTML::

    <script src="{{ url_for('static', filename='js/components/mapWidget.js') }}"></script>

Initialize in page script::

    <div id="mapContainer"></div>
    <script>
        const mapWidget = new MapWidget('mapContainer', {
            center: [51.5074, -0.1278],  // London
            zoom: 13
        });
        mapWidget.loadShops();
    </script>

**Key Functions**:

- ``MapWidget(container, options)``: Initialize map
- ``loadShops()``: Fetch and display all barbershop locations
- ``filterByLocation(searchTerm)``: Filter shops by location
- ``centerOnShop(shopId)``: Center map on specific shop
- ``showPopup(marker)``: Display shop info popup

**API Endpoints Used**:

- ``GET /api/barbershops``: Get list of barbershops
- ``GET /api/barbershops/<id>``: Get shop details

**Features**:

- Real-time location updates
- Search by location name or postcode
- Click marker for shop details
- Responsive on mobile and desktop
- Touch gestures for mobile navigation

The script in app/static/js/components/mapWidget.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/barbershops to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/mapWidget.js` provides frontend browser behavior. Function responsibilities: `initMapWidget` initializes the Leaflet map instance and base layers; `renderShops` renders barbershop markers and popup content on the map.
