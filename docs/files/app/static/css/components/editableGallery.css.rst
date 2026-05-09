editableGallery.css - Editable Gallery Component Styles
=====================================================

**Purpose**: Styles for gallery editing interface where barbers upload and manage photos.

**What it styles**:

- Edit mode gallery grid
- Photo upload zone within gallery
- Edit/delete buttons on photos
- Drag-to-reorder functionality
- Photo caption editing
- Gallery management UI

**How to use**:

Include in CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/editableGallery.css') }}">

HTML structure::

    <div class="editable-gallery">
        <div class="gallery-edit-controls">
            <button class="btn-add-photo">+ Add Photo</button>
        </div>
        <div class="gallery-items-editable">
            <div class="gallery-item-editable" draggable="true">
                <img src="photo.jpg" />
                <div class="edit-controls">
                    <button class="btn-edit">Edit</button>
                    <button class="btn-delete">Delete</button>
                </div>
            </div>
        </div>
    </div>

**Key CSS Classes**:

- ``.editable-gallery``: Container
- ``.gallery-item-editable``: Individual photo in edit mode
- ``.edit-controls``: Edit/delete button container
- ``.photo-caption-edit``: Caption input field
- ``.dragging``: Photo being dragged

**Features**:

- Drag-and-drop reordering
- Quick delete buttons
- Edit captions inline
- Batch upload support
- Visual feedback on drag
- Responsive layout

app/static/css/components/editableGallery.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. Its rules provide the base visual treatment used when rendering the related template/components. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the editableGallery component. It styles selectors such as .editable-gallery-card, .editable-gallery-card__media, .editable-gallery-card__media img, and .editable-gallery-card__edit-btn.
