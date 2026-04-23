app/static/js/components/editableUserPromo.js
=============================================

Overview
--------

The script in app/static/js/components/editableUserPromo.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/user/profile-photo and /api/user/profile to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/editableUserPromo.js` provides frontend browser behavior. Function responsibilities: `createEditableUserPromo` creates editable user promo; `escapeHtml` helper function to escape HTML.