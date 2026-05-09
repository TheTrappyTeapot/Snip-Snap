barberGallery.js - Barber Gallery Component
==========================================

**Purpose**: Component for displaying and managing barber portfolio gallery.

**What it does**:

- Renders barber's work photo gallery
- Manages photo display in grid
- Handles lightbox/expanded view
- Manages photo interactions
- Shows photo metadata (date, style)
- Handles load states
- Manages error handling
- Supports photo filtering by style

**How to use**:

Include in page::

    <script src="{{ url_for('static', filename='js/components/barberGallery.js') }}"></script>

Initialize gallery::

    const gallery = new BarberGallery('galleryContainer', barberId);
    gallery.load();
    gallery.onPhotoClick((photo) => showLightbox(photo));

**Key Functions**:

- ``BarberGallery(container, barberId)``: Initialize
- ``load()``: Fetch photos from API
- ``render()``: Display gallery
- ``openLightbox(photoIndex)``: Expand photo
- ``closeLightbox()``: Close expanded view
- ``nextPhoto()``: Show next photo
- ``previousPhoto()``: Show previous photo
- ``filterByStyle(style)``: Filter gallery
- ``sortBy(criterion)``: Sort photos

**API Endpoints**:

- ``GET /api/gallery/<barber_id>``: Get barber photos

**Features**:

- Grid layout
- Lightbox viewer
- Style filtering
- Photo metadata
- Date sorting
- Error states
- Loading indicators
- Responsive design
- Touch gestures
- Keyboard navigation