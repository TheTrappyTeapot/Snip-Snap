app/static/js/components/mapWidget.js
=====================================

Overview
--------

The script in app/static/js/components/mapWidget.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/barbershops to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/mapWidget.js` provides frontend browser behavior. Function responsibilities: `initMapWidget` initializes the Leaflet map instance and base layers; `renderShops` renders barbershop markers and popup content on the map.
