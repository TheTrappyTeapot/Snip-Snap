app/static/js/pages/profile.js
==============================

Overview
--------

The script in app/static/js/pages/profile.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/user/barbershops, /api/user/current-barbershop, and /api/user/profile to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/pages/profile.js` provides frontend browser behavior. Function responsibilities: `initializeForm` initializes profile form controls when the DOM is ready; `clearErrors` clears field-level and general profile form error messages; `validateForm` validates profile form values and reports any field-level errors; `openModal` opens the profile modal dialog; `closeModal` closes the profile modal dialog.
