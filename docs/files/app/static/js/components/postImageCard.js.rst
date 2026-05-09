postImageCard.js - Post Image Card Component
==========================================

**Purpose**: Individual photo card for gallery posts with interactions.

**What it does**:

- Renders photo post card
- Manages like/favorite functionality
- Shows barber information
- Handles image loading
- Displays ratings and metadata
- Manages click/hover interactions
- Shows action buttons on hover

**How to use**:

Include in page::

    <script src="{{ url_for('static', filename='js/components/postImageCard.js') }}"></script>

Create and render::

    const card = new PostImageCard(postData, container);
    card.render();
    card.onLike(() => updateLikeCount());
    card.onBarberClick(() => goToProfile());

**Key Functions**:

- ``PostImageCard(data, container)``: Initialize
- ``render()``: Display card
- ``updateLikeCount(count)``: Update like display
- ``showOverlay()``: Show action buttons
- ``hideOverlay()``: Hide overlay
- ``openFullImage()``: Show expanded view

**Features**:

- Like/unlike toggle
- Like counter
- Barber name link
- Rating display
- Image hover effects
- Action button overlay
- Share options

The script in app/static/js/components/postImageCard.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/postImageCard.js` provides frontend browser behavior.