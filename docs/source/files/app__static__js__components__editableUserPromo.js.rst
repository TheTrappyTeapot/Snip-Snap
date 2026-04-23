app/static/js/components/editableUserPromo.js
=============================================

Overview
--------

The script in app/static/js/components/editableUserPromo.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/user/profile-photo and /api/user/profile to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This UI component script powers editableUserPromo behavior on the client side. It organizes logic through functions such as createEditableUserPromo, escapeHtml, uploadProfilePhoto, and saveUsername.
