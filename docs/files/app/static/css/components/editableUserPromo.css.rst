editableUserPromo.css - Editable User Profile Card Styles
========================================================

**Purpose**: Styles for editable user profile card (when user is editing their own profile).

**What it styles**:

- Edit mode profile card
- Input fields for profile info
- Profile photo upload trigger
- Bio/description editing area
- Save/Cancel buttons
- Form validation styling
- Preview of changes

**How to use**:

Include in CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/editableUserPromo.css') }}">

HTML structure::

    <div class="user-promo-editable">
        <button class="btn-change-photo">Change Photo</button>
        <input type="text" class="input-name" value="John" />
        <textarea class="input-bio">Bio...</textarea>
        <div class="form-actions">
            <button class="btn-save">Save</button>
            <button class="btn-cancel">Cancel</button>
        </div>
    </div>

**Key CSS Classes**:

- ``.user-promo-editable``: Edit mode container
- ``.input-name``: Name input field
- ``.input-bio``: Bio textarea
- ``.btn-change-photo``: Photo upload button
- ``.form-actions``: Save/Cancel buttons
- ``.error``: Validation error state

**Features**:

- Inline editing
- Photo upload trigger
- Form validation feedback
- Save/Cancel options
- Real-time preview
- Character count for bio

app/static/css/components/editableUserPromo.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. It includes 1 media query block(s) to adapt the interface across viewport sizes. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the editableUserPromo component. It styles selectors such as .hidden, .editable-user-promo, .editable-user-promo__avatar-wrapper, and .editable-user-promo__avatar.
