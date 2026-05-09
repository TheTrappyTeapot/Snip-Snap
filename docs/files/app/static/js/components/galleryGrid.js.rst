galleryGrid.js - Gallery Grid Layout Component
==============================================

**Purpose**: Responsive grid layout for photo galleries.

**What it does**:

- Manages responsive grid layout
- Handles column count based on screen size
- Manages gap and spacing
- Handles window resize events
- Manages image loading state
- Smooth animations on load

**How to use**:

Include in page::

    <script src="{{ url_for('static', filename='js/components/galleryGrid.js') }}"></script>

Initialize grid::

    const grid = new GalleryGrid(container, {
        minWidth: 250,
        gap: 16,
        responsive: true
    });
    grid.addItems(photoCards);

**Key Functions**:

- ``GalleryGrid(container, options)``: Initialize
- ``addItems(items)``: Add to grid
- ``removeItem(item)``: Remove from grid
- ``recalculate()``: Recalculate layout
- ``setColumnCount(count)``: Set column number
- ``animate()``: Smooth transitions

**Responsive Behavior**:

- Auto-adjusts columns on resize
- Maintains aspect ratio
- Smooth reflow animation
- Mobile optimized

**Features**:

- Flexible grid
- Responsive columns
- Custom gap spacing
- Image lazy loading
- Smooth animations
- Touch-friendly

The script in app/static/js/components/galleryGrid.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/galleryGrid.js` provides frontend browser behavior.