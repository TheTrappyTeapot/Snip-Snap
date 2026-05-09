barberGallery.css - Barber Gallery Component Styles
===================================================

**Purpose**: Styles for displaying a barber's photo gallery/portfolio.

**What it styles**:

- Grid layout for displaying haircut photos
- Photo cards with thumbnails and metadata
- Image hover effects and overlays
- Responsive grid that adjusts columns on different screen sizes
- Gallery navigation and pagination controls

**How to use**:

Include in base template CSS links::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/barberGallery.css') }}">

HTML structure::

    <div class="barber-gallery">
        <div class="gallery-grid">
            <div class="gallery-item">
                <img src="photo.jpg" alt="Haircut" />
                <p class="gallery-caption">Fade Haircut</p>
            </div>
        </div>
    </div>

**Key CSS Classes**:

- ``.barber-gallery``: Main container
- ``.gallery-grid``: Grid layout wrapper
- ``.gallery-item``: Individual photo card
- ``.gallery-caption``: Photo description
- ``.gallery-overlay``: Hover overlay effect

**Responsive Design**:

- Mobile: 1-2 columns
- Tablet: 2-3 columns
- Desktop: 3-4 columns

**Features**:

- Image lazy loading for performance
- Hover zoom effect on photos
- Click to view full size
- Smooth transitions between states

app/static/css/components/barberGallery.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. Its rules provide the base visual treatment used when rendering the related template/components. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the barberGallery component. It styles selectors such as .barber-gallery, .barber-gallery__title, .barber-gallery__grid, and .barber-gallery__cell.
