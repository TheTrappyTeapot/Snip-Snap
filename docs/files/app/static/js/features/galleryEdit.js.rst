galleryEdit.js - Gallery Photo Editing Feature
==============================================

**Purpose**: Feature for editing gallery photos (reorder, delete, edit captions).

**What it does**:

- Manages all photo editing operations
- Handles drag-to-reorder photos
- Manages batch photo deletion
- Edits photo captions inline
- Communicates with editableGallery component
- Syncs changes to backend
- Handles undo/redo
- Shows edit status

**How to use**:

Initialize in dashboard::

    const galleryEditor = new GalleryEditFeature('galleryContainer', barberId);
    galleryEditor.init();
    galleryEditor.onSave(() => showSuccessMessage());

**Key Functions**:

- ``GalleryEditFeature(container, barberId)``: Initialize
- ``init()``: Load and setup
- ``reorderPhotos(newOrder)``: Drag operation
- ``deletePhoto(photoId)``: Remove photo
- ``editCaption(photoId, newCaption)``: Change caption
- ``save()``: Persist all changes
- ``undo()``: Revert changes
- ``cancel()``: Exit edit mode

**API Endpoints**:

- ``PUT /api/gallery/reorder``: Save photo order
- ``DELETE /api/photo/<id>``: Delete photo
- ``PATCH /api/photo/<id>/caption``: Update caption

**Features**:

- Drag-to-reorder
- Inline caption editing
- Multi-photo delete
- Undo functionality
- Change preview
- Bulk operations
- Confirmation dialogs

The script in app/static/js/features/galleryEdit.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/photos/replace, /api/photos/upload, and /api/my-photos to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/features/galleryEdit.js` provides frontend browser behavior. Function responsibilities: `initAddGalleryPhotoForm` initializes add gallery photo form; `resetEditPhotoForm` resets edit photo form; `showEditPhotoError` shows edit photo error; `showEditPhotoSuccess` shows edit photo success; `hideEditPhotoMessages` hides edit photo messages; `showEditPhotoLoading` shows edit photo loading; `resetAddGalleryPhotoForm` resets add gallery photo form; `showAddGalleryPhotoError` shows add gallery photo error; `showAddGalleryPhotoSuccess` shows add gallery photo success; `hideAddGalleryPhotoMessages` hides add gallery photo messages; `showAddGalleryPhotoLoading` shows add gallery photo loading.