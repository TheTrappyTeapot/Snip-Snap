app/static/js/features/uploadPost.js
====================================

Overview
--------

The script in app/static/js/features/uploadPost.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/discover/search_items and /api/photos/upload to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/features/uploadPost.js` provides frontend browser behavior. Function responsibilities: `resetForm` resets form; `showError` shows error; `showSuccess` shows success; `hideMessages` hides messages; `showLoading` shows loading.