app/static/js/components/mapWidget.js
=====================================

Overview
--------

The script in app/static/js/components/mapWidget.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/barbershops to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This UI component script powers mapWidget behavior on the client side. It organizes logic through functions such as initMapWidget and renderShops.
