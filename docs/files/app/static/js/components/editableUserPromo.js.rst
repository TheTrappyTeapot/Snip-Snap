editableUserPromo.js - Editable User Profile Card Component
========================================================

**Purpose**: JavaScript for editing user profile information card.

**What it does**:

- Manages form for editing user profile
- Handles profile photo upload
- Validates input fields
- Saves changes to API
- Manages edit/view modes
- Shows validation feedback
- Handles loading states

**How to use**:

Include in dashboard::

    <script src="{{ url_for('static', filename='js/components/editableUserPromo.js') }}"></script>

Initialize editor::

    const editor = new EditableUserPromo('profileContainer', userId);
    editor.enableEdit();

**Key Functions**:

- ``EditableUserPromo(container, userId)``: Initialize
- ``enableEdit()``: Enter edit mode
- ``disableEdit()``: Cancel editing
- ``uploadPhoto(file)``: Change profile photo
- ``updateBio(text)``: Change bio
- ``save()``: Save all changes
- ``validate()``: Check form validity

**API Endpoints**:

- ``PUT /api/profile``: Update user info
- ``POST /api/upload-photo``: Upload profile photo

**Features**:

- Edit mode toggle
- Photo upload
- Bio text area
- Form validation
- Character count
- Save/Cancel buttons
- Error messages

The script in app/static/js/components/editableUserPromo.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/user/profile-photo and /api/user/profile to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/editableUserPromo.js` provides frontend browser behavior. Function responsibilities: `createEditableUserPromo` creates editable user promo; `escapeHtml` helper function to escape HTML.