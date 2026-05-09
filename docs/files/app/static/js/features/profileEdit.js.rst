profileEdit.js - Profile Editing Feature
=======================================

**Purpose**: Feature for editing user/barber profile information.

**What it does**:

- Manages profile form
- Handles photo upload
- Validates all inputs
- Saves changes to API
- Manages loading states
- Shows validation errors
- Handles success/error feedback
- Manages cancel/reset

**How to use**:

Initialize in dashboard::

    const profileEditor = new ProfileEditFeature('profileForm', userId);
    profileEditor.load();
    profileEditor.onSave(() => showSuccess());

**Key Functions**:

- ``ProfileEditFeature(container, userId)``: Initialize
- ``load()``: Fetch current profile
- ``validate()``: Check form validity
- ``uploadPhoto(file)``: Change profile photo
- ``save()``: Save all changes
- ``cancel()``: Revert to original
- ``reset()``: Clear form

**Form Fields**:

- Username (if barber: name)
- Bio/description
- Location/postcode
- Email
- Phone (if barber)
- Social links (if barber)
- Profile photo

**API Endpoints**:

- ``GET /api/profile``: Get current info
- ``PUT /api/profile``: Save changes
- ``POST /api/upload-photo``: Upload photo

**Features**:

- Form validation
- Photo upload
- Field feedback
- Save/Cancel buttons
- Loading states
- Error messages

The script in app/static/js/features/profileEdit.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/features/profileEdit.js` provides frontend browser behavior.