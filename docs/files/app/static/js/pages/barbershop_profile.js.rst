barbershop_profile.js - Barbershop Profile Page Script
===================================================

**Purpose**: Manages barbershop profile page display and interactions.

**What it does**:

- Loads barbershop information (name, location, hours, rating)
- Displays shop photo and gallery
- Shows list of barbers/staff
- Shows embedded map
- Displays customer reviews
- Shows contact information
- Manages navigation to barber profiles
- Handles error states

**How to use**:

Include in shop profile page::

    <script src="{{ url_for('static', filename='js/pages/barbershop_profile.js') }}"></script>

**Key Functions**:

- ``initShopProfile(shopId)``: Initialize page
- ``loadShopInfo(shopId)``: Fetch shop data
- ``loadStaff(shopId)``: Get barber list
- ``loadGallery(shopId)``: Get shop photos
- ``loadReviews(shopId)``: Get reviews
- ``initMap(location)``: Show map
- ``goToBarberProfile(barberId)``: Navigate to barber

**API Endpoints**:

- ``GET /api/barbershop/<id>``: Get shop info
- ``GET /api/barbershop/<id>/staff``: Get staff
- ``GET /api/gallery/shop/<id>``: Get photos
- ``GET /api/reviews/shop/<id>``: Get reviews

**Page Elements**:

- Shop photo and info
- Opening hours
- Staff cards (clickable)
- Photo gallery
- Embedded map
- Reviews section
- Contact buttons

**Features**:

- Shop hours display
- Open/closed status
- Staff member links
- Location on map
- Reviews with ratings
- Call/email buttons
- Share shop

The script in app/static/js/pages/barbershop_profile.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/pages/barbershop_profile.js` provides frontend browser behavior.