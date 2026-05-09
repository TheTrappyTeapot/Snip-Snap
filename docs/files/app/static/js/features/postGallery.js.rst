app/static/js/features/postGallery.js
=====================================

Overview
--------

The script in app/static/js/features/postGallery.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/gallery/posts to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/features/postGallery.js` provides frontend browser behavior. Function responsibilities: `normaliseTagListItems` groups selected tag-list entries into filter/tag/barber/barbershop ID arrays; `resolveEffectiveSort` determines whether sorting should be `most_recent`, `closest`, `highest_rated`, or blended based on active filters; `createGalleryLoader` creates the loading indicator element shown while requests are in flight; `setLoadingVisible` toggles loader visibility for fetch states; `render` draws either empty/error states or the gallery grid for current items; `buildPayload` assembles the API request body from current filter state and pagination cursor; `payloadKey` builds a stable serialized key used to detect filter-state changes across page loads.
