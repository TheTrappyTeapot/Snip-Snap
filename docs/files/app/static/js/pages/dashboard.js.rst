dashboard.js - Barber Dashboard Page Script
==========================================

**Purpose**: Manages the barber dashboard interface for profile and shop management.

**What it does**:

- Loads barber profile and shop information
- Manages profile editing and updates
- Handles working hours/schedule updates
- Displays gallery management interface
- Shows customer reviews and ratings
- Handles analytics and statistics
- Manages barbershop information

**How to use**:

Include in dashboard page::

    <script src="{{ url_for('static', filename='js/pages/dashboard.js') }}"></script>

**Key Functions**:

- ``loadDashboard(barberId)``: Initialize dashboard
- ``editProfile()``: Enable profile editing
- ``saveProfile(data)``: Save profile changes
- ``updateSchedule(schedule)``: Update working hours
- ``getAnalytics()``: Fetch dashboard stats
- ``manageBarbershop()``: Edit barbershop details

**API Endpoints**:

- ``GET /api/profile/<barber_id>``: Get barber info
- ``PUT /api/profile``: Update profile
- ``GET /api/schedule/<barber_id>``: Get schedule
- ``PUT /api/schedule``: Update working hours
- ``GET /api/analytics``: Get statistics

**Dashboard Sections**:

- **Profile**: Edit photo, bio, contact info
- **Barbershop**: Edit shop name, hours, location
- **Gallery**: Upload/manage haircut photos
- **Reviews**: View customer feedback
- **Analytics**: View statistics (views, bookings, etc.)
- **Schedule**: Manage working hours

**Features**:

- Real-time profile updates
- Photo upload interface
- Schedule calendar view
- Review ratings display
- Social media links
- Availability status toggle

The script in app/static/js/pages/dashboard.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/pages/dashboard.js` provides frontend browser behavior. Function responsibilities: `initializeFeatures` sets up dashboard feature modules when the DOM is ready.
