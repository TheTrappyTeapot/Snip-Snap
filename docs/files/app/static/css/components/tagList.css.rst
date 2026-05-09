tagList.css - Tag List Component Styles
======================================

**Purpose**: Styles for displaying and managing tags/categories.

**What it styles**:

- Tag/chip container and layout
- Individual tag styling
- Tag colors and variants
- Remove button on tags
- Tag hover/active states
- Responsive tag wrapping

**How to use**:

Include in CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/tagList.css') }}">

HTML structure::

    <div class="tag-list">
        <span class="tag">
            Fade
            <button class="tag-remove">×</button>
        </span>
        <span class="tag">Undercut</span>
        <span class="tag">Modern</span>
    </div>

**Key CSS Classes**:

- ``.tag-list``: Container
- ``.tag``: Individual tag
- ``.tag.primary``: Primary color tag
- ``.tag.secondary``: Secondary color tag
- ``.tag-remove``: Remove button
- ``.tag--large``: Large tag variant

**Features**:

- Multiple tag variants
- Remove buttons (optional)
- Color-coded tags
- Responsive wrapping
- Hover effects
- Click to select/filter

app/static/css/components/tagList.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. Its rules provide the base visual treatment used when rendering the related template/components. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the tagList component. It styles selectors such as .taglist, .taglist p, .taglist ul, and .taglist li.
