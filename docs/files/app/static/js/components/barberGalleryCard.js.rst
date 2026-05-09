barberGalleryCard.js - Individual Gallery Card Component
=======================================================

**Purpose**: JavaScript for individual photo card interactions and display.

**What it does**:

- Renders individual gallery photo card
- Handles image lazy loading
- Manages like/favorite button
- Shows barber information on hover
- Handles card click to view full image
- Loads image metadata from API
- Manages card animations

**How to use**:

Include in page::

    <script src="{{ url_for('static', filename='js/components/barberGalleryCard.js') }}"></script>

Create and render cards::

    const card = new GalleryCard(photoData, container);
    card.render();
    card.onLike(() => console.log('Liked!'));

**Key Functions**:

- ``GalleryCard(data, container)``: Initialize card
- ``render()``: Display card in DOM
- ``setImage(url)``: Load image
- ``toggleLike()``: Like/unlike photo
- ``showDetails()``: Show full details
- ``destroy()``: Remove from DOM

**Features**:

- Lazy image loading
- Like button with count
- Hover effects
- Image caption
- Barber name and rating
- Share button
- Click to expand

The script in app/static/js/components/barberGalleryCard.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/barberGalleryCard.js` provides frontend browser behavior.