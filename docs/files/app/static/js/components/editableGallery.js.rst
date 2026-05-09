editableGallery.js - Editable Gallery Management Component
=========================================================

**Purpose**: JavaScript for managing gallery photos (upload, delete, reorder).

**What it does**:

- Handles drag-and-drop photo reordering
- Manages photo upload interface
- Implements delete functionality
- Handles photo caption editing
- Updates API with changes
- Manages loading states
- Handles errors gracefully

**How to use**:

Include in dashboard::

    <script src="{{ url_for('static', filename='js/components/editableGallery.js') }}"></script>

Initialize editor::

    const gallery = new EditableGallery('galleryContainer', {
        barberId: 123,
        canDelete: true,
        canReorder: true
    });

**Key Functions**:

- ``EditableGallery(container, options)``: Initialize
- ``loadPhotos(barberId)``: Fetch photos from API
- ``addPhoto(file)``: Upload new photo
- ``deletePhoto(photoId)``: Remove photo
- ``reorderPhotos(newOrder)``: Save new order
- ``updateCaption(photoId, caption)``: Edit caption
- ``saveChanges()``: Persist to backend

**Drag & Drop**:

- Drag photos to reorder
- Visual feedback during drag
- Drop to apply new order
- Auto-save after drop

**Features**:

- Batch upload
- Drag to reorder
- Edit captions
- Quick delete
- Upload progress
- Error recovery

The script in app/static/js/components/editableGallery.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/editableGallery.js` provides frontend browser behavior.