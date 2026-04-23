app/static/js/pages/signup.js
=============================

Overview
--------

The script in app/static/js/pages/signup.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/auth/create-user to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/pages/signup.js` provides frontend browser behavior. Function responsibilities: `initializeForm` initialize form when DOM is ready; `clearErrors` clears all visible validation and general error messages; `validateForm` validates signup inputs and returns true when the form is valid.