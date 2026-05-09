tagList.js - Tag List Management Component
========================================

**Purpose**: Display and manage tag/category selections.

**What it does**:

- Renders tag list
- Manages tag selection/deselection
- Handles tag removal
- Updates tag state
- Manages tag filtering
- Emits events on tag changes
- Supports drag-to-reorder

**How to use**:

Include in page::

    <script src="{{ url_for('static', filename='js/components/tagList.js') }}"></script>

Initialize and manage tags::

    const tags = new TagList('tagContainer');
    tags.addTag('Fade');
    tags.addTag('Undercut');
    tags.setSelected(['Fade']);
    tags.onChange((selected) => console.log(selected));

**Key Functions**:

- ``TagList(container, options)``: Initialize
- ``addTag(text, value)``: Add new tag
- ``removeTag(value)``: Remove tag
- ``setSelected(values)``: Mark as selected
- ``getSelected()``: Get selected tags
- ``clear()``: Clear all selections
- ``disable()``: Disable interactions

**Features**:

- Add/remove tags
- Click to toggle selection
- Multiple selections
- Tag colors/variants
- Remove buttons
- Custom data values
- Event callbacks
- Keyboard support

The script in app/static/js/components/tagList.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/tagList.js` provides frontend browser behavior.