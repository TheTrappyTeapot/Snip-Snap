app/static/js/features/galleryEdit.js
=====================================

Overview
--------

The script in app/static/js/features/galleryEdit.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/photos/replace, /api/photos/upload, and /api/my-photos to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This feature orchestration script powers galleryEdit behavior on the client side. It organizes logic through functions such as initGalleryEditFeature, initAddGalleryPhotoForm, submitAddGalleryPhoto, loadEditableGallery, and openEditPhotoModal.
