app/static/js/pages/profile.js
==============================

Overview
--------

The script in app/static/js/pages/profile.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/user/barbershops, /api/user/current-barbershop, and /api/user/profile to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This page controller powers profile behavior on the client side. It organizes logic through functions such as initializeForm, loadBarbershops, initializeBarbershopAutocomplete, loadCurrentBarbershop, and updateBarbershopFieldVisibility.
