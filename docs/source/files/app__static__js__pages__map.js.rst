app/static/js/pages/map.js
==========================

Overview
--------

The script in app/static/js/pages/map.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/user/location and /api/barbershops to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/pages/map.js` provides frontend browser behavior. Function responsibilities: `placeUserMarker` ── User location marker (red circle) ───────────────────────────────────────; `showModal` ── Location modal ───────────────────────────────────────────────────────────; `hideModal` hides modal; `showSavePrompt` ── Save location prompt ─────────────────────────────────────────────────────; `hideSavePrompt` hides save prompt; `haversineKm` ── Helpers ──────────────────────────────────────────────────────────────────; `formatDistance` returns format distance; `escapeHtml` ── HTML escaping to prevent XSS in popups ───────────────────────────────────; `buildPopupHtml` ── Barbershop popup (shows shop info with go to shop button) ────────────────; `addMarkers` leaflet handles click-to-open/close automatically.