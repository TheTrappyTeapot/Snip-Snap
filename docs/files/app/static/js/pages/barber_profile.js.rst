barber_profile.js - Barber Profile Page Script
============================================

**Purpose**: Manages barber profile page display and interactions.

**What it does**:

- Loads barber profile data from API
- Displays barber information (bio, photo, rating)
- Shows gallery of work
- Displays working hours schedule
- Shows customer reviews
- Manages follow/unfollow button
- Handles navigation to book/contact
- Manages error handling

**How to use**:

Include in barber profile page::

    <script src="{{ url_for('static', filename='js/pages/barber_profile.js') }}"></script>

**Key Functions**:

- ``initBarberProfile(barberId)``: Initialize page
- ``loadBarberInfo(barberId)``: Fetch barber data
- ``loadGallery(barberId)``: Get photos
- ``loadReviews(barberId)``: Get reviews
- ``toggleFollow(barberId)``: Follow/unfollow
- ``renderProfile(data)``: Display data
- ``handleBooking()``: Navigate to booking

**API Endpoints**:

- ``GET /api/barber/<id>``: Get barber info
- ``GET /api/gallery/<barber_id>``: Get photos
- ``GET /api/reviews/<barber_id>``: Get reviews
- ``POST /api/follow``: Follow barber

**Page Elements**:

- Profile header with photo
- Bio and rating
- Gallery grid
- Schedule/hours
- Review section
- Follow button
- Contact/booking button

**Features**:

- Auto-load page data
- Follow/unfollow
- Gallery scrollable
- Reviews paginated
- Share profile
- Contact methods

The script in app/static/js/pages/barber_profile.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/pages/barber_profile.js` provides frontend browser behavior.