map.js - Interactive Map Page Script
==================================

**Purpose**: Manages interactive map display and barbershop location browsing.

**What it does**:

- Initializes Leaflet/Google Maps
- Loads barbershop locations from API
- Adds markers for each location
- Handles marker click to show details
- Manages search/filtering
- Syncs map with sidebar list
- Handles map navigation
- Shows current user location
- Handles location-based features

**How to use**:

Include in map page::

    <script src="{{ url_for('static', filename='js/pages/map.js') }}"></script>

**Key Functions**:

- ``initMap(containerId)``: Initialize map
- ``loadShops()``: Fetch locations from API
- ``addMarker(shop)``: Add shop marker
- ``centerOnShop(shopId)``: Center map
- ``filterByLocation(query)``: Search shops
- ``filterByDistance(radius)``: Show nearby
- ``showPopup(marker)``: Display shop info
- ``goToShop(shopId)``: Navigate to profile

**API Endpoints**:

- ``GET /api/barbershops``: Get all shops
- ``GET /api/barbershops?location=<query>``: Search
- ``GET /api/barbershops?distance=<km>``: Nearby

**Map Features**:

- Markers for shops
- Info popups on click
- Search/filter
- Distance filtering
- Current location
- Directions link
- Sidebar with list

**Interactions**:

- Click marker: Show popup
- Click item in list: Center map
- Search: Filter visible shops
- Zoom in/out
- Pan around
- "Directions" button

The script in app/static/js/pages/map.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/user/location and /api/barbershops to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/pages/map.js` provides frontend browser behavior. Function responsibilities: `placeUserMarker` draws the user's current marker on the map; `showModal` opens the location permission modal; `hideModal` closes the location permission modal; `showSavePrompt` displays the save-location confirmation prompt; `hideSavePrompt` hides the save-location confirmation prompt; `haversineKm` computes distance in kilometers between two coordinates; `formatDistance` formats distance values for display; `escapeHtml` escapes popup text to prevent HTML injection; `buildPopupHtml` builds barbershop popup markup with distance and action controls; `addMarkers` renders map markers and binds popup interactions.
