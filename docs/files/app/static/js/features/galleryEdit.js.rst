app/static/js/features/galleryEdit.js
=====================================

Overview
--------

The script in app/static/js/features/galleryEdit.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/photos/replace, /api/photos/upload, and /api/my-photos to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/features/galleryEdit.js` provides frontend browser behavior. Function responsibilities: `initAddGalleryPhotoForm` initializes add gallery photo form; `resetEditPhotoForm` resets edit photo form; `showEditPhotoError` shows edit photo error; `showEditPhotoSuccess` shows edit photo success; `hideEditPhotoMessages` hides edit photo messages; `showEditPhotoLoading` shows edit photo loading; `resetAddGalleryPhotoForm` resets add gallery photo form; `showAddGalleryPhotoError` shows add gallery photo error; `showAddGalleryPhotoSuccess` shows add gallery photo success; `hideAddGalleryPhotoMessages` hides add gallery photo messages; `showAddGalleryPhotoLoading` shows add gallery photo loading.