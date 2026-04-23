app/static/js/pages/map.js
==========================

Overview
--------

The script in app/static/js/pages/map.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/user/location and /api/barbershops to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/pages/map.js` provides frontend browser behavior. Function responsibilities: `placeUserMarker` draws the user's current marker on the map; `showModal` opens the location permission modal; `hideModal` closes the location permission modal; `showSavePrompt` displays the save-location confirmation prompt; `hideSavePrompt` hides the save-location confirmation prompt; `haversineKm` computes distance in kilometers between two coordinates; `formatDistance` formats distance values for display; `escapeHtml` escapes popup text to prevent HTML injection; `buildPopupHtml` builds barbershop popup markup with distance and action controls; `addMarkers` renders map markers and binds popup interactions.
