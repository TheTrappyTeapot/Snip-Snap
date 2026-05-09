editableGalleryCard.js - Editable Gallery Card Component
=======================================================

**Purpose**: Individual photo card component in edit mode (with delete/edit controls).

**What it does**:

- Renders photo card with edit controls
- Manages drag handle for reordering
- Shows delete button
- Handles edit interactions
- Manages photo state
- Provides feedback on actions

**How to use**:

Use within EditableGallery component::

    const card = new EditableGalleryCard(photoData, container);
    card.render();
    card.onDelete(() => { /* remove photo */ });
    card.onReorder(() => { /* save order */ });

**Key Functions**:

- ``EditableGalleryCard(data, container)``: Initialize
- ``render()``: Display card
- ``delete()``: Remove photo
- ``edit()``: Open edit mode
- ``setDragging(bool)``: Drag state
- ``updateCaption(text)``: Change caption

**Features**:

- Drag handle
- Delete button
- Edit caption inline
- Loading state
- Error state
- Hover effects
- Delete confirmation

The script in app/static/js/components/editableGalleryCard.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/editableGalleryCard.js` provides frontend browser behavior.