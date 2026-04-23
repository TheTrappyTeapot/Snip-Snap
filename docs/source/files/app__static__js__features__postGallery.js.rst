app/static/js/features/postGallery.js
=====================================

Overview
--------

The script in app/static/js/features/postGallery.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/gallery/posts to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/features/postGallery.js` provides frontend browser behavior. Function responsibilities: `normaliseTagListItems` normalizes tag list items list; `resolveEffectiveSort` resolves effective sort; `createGalleryLoader` creates gallery loader; `setLoadingVisible` sets loading visible; `render` renders UI output; `buildPayload` builds payload; `payloadKey` returns payload key.