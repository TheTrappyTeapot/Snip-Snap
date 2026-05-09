galleryGrid.css - Gallery Grid Layout Styles
===========================================

**Purpose**: Responsive grid layout system for displaying photo galleries.

**What it styles**:

- Grid container and items
- Responsive column count
- Gap/spacing between items
- Masonry-style layout option
- Image aspect ratio maintenance
- Grid animations and transitions

**How to use**:

Include in CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/galleryGrid.css') }}">

HTML structure::

    <div class="gallery-grid" data-columns="3">
        <div class="gallery-grid-item">
            <img src="photo.jpg" />
        </div>
        <div class="gallery-grid-item">
            <img src="photo2.jpg" />
        </div>
    </div>

**Key CSS Classes**:

- ``.gallery-grid``: Grid container
- ``.gallery-grid-item``: Individual grid cell
- ``.gallery-grid--2col``: 2-column layout
- ``.gallery-grid--3col``: 3-column layout
- ``.gallery-grid--4col``: 4-column layout

**Responsive Breakpoints**:

- Mobile: 1-2 columns
- Tablet: 2-3 columns
- Desktop: 3-4 columns
- Wide: 4-6 columns

**Features**:

- Flexible grid system
- Maintains image aspect ratio
- Smooth animations
- Gap/gutter control
- Auto-responsive columns

app/static/css/components/galleryGrid.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. Its rules provide the base visual treatment used when rendering the related template/components. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the galleryGrid component. It styles selectors such as .galleryGrid and .galleryGrid__cell.
