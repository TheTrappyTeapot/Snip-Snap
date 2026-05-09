map.html - Interactive Map Page Template
========================================

**Purpose**: Interactive map showing barbershop locations.

**What it contains**:

- Full-screen map canvas
- Barbershop location markers
- Sidebar with shop list
- Search/filter controls
- Location info popups
- Zoom and pan controls

**How it works**:

Page displays an interactive map with all barbershop locations marked. Users can click markers to see shop details, search by location, and navigate to shop profiles.

**Key Sections**:

1. **Map Canvas**: Leaflet/Google Maps showing locations
2. **Markers**: Pin for each barbershop
3. **Sidebar**: Scrollable list of shops
4. **Search Bar**: Find shops by location/name
5. **Info Popup**: Shop details on marker click

**Marker Information** (popup shows):

- Shop name
- Address and postcode
- Phone number
- Hours of operation
- Average rating
- "View Shop" button

**Interactions**:

- **Click Marker**: Show shop popup
- **Click Shop in List**: Center map on shop
- **Search**: Filter visible shops
- **Zoom In/Out**: Detail level control
- **Pan**: Drag map to explore

**Mobile Features**:

- Sidebar collapses to bottom sheet
- Touch gestures for navigation
- Location-based auto-center
- Close popup on outside click

**Links**:

Click "View Shop" to navigate to:

- Barbershop profile page
- Barber profiles
- Reviews and ratings
- Opening hours
- Contact information===

Overview
--------

app/templates/pages/map.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It composes display sections for content rendering and component mounting points used by client scripts. Client behavior is attached through script includes such as leaflet.js, template-resolved JavaScript assets, and template-resolved JavaScript assets, which connect this template to JavaScript page logic.

Purpose
-------

This template renders the map view for the web application. It extends base.html to inherit shared layout and asset structure.
