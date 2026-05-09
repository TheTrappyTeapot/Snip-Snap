profile.js - User Profile Page Script
===================================

**Purpose**: Manages user profile page for customers.

**What it does**:

- Loads user profile information
- Displays profile photo and stats
- Shows saved/favorite posts
- Shows followed barbers list
- Manages edit profile button
- Handles logout
- Manages account settings
- Shows activity history

**How to use**:

Include in user profile page::

    <script src="{{ url_for('static', filename='js/pages/profile.js') }}"></script>

**Key Functions**:

- ``initProfilePage(userId)``: Initialize page
- ``loadProfile(userId)``: Fetch user data
- ``loadSaved(userId)``: Get favorite posts
- ``loadFollowing(userId)``: Get followed barbers
- ``loadActivity(userId)``: Get activity history
- ``openEditProfile()``: Show edit form
- ``logout()``: Sign out user

**API Endpoints**:

- ``GET /api/profile``: Get user info
- ``GET /api/profile/saved``: Get favorites
- ``GET /api/profile/following``: Get follows
- ``GET /api/profile/activity``: Get history

**Page Sections**:

- **Header**: User photo, name, stats
- **Tabs**: Favorites, Following, Activity, Settings
- **Favorites**: Grid of saved posts
- **Following**: List of followed barbers
- **Activity**: Recent interactions
- **Settings**: Account preferences

**Features**:

- View saved posts
- View followed barbers
- Edit profile
- Change password
- Account settings
- Activity log
- Logout button

The script in app/static/js/pages/profile.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/user/barbershops, /api/user/current-barbershop, and /api/user/profile to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/pages/profile.js` provides frontend browser behavior. Function responsibilities: `initializeForm` initializes profile form controls when the DOM is ready; `clearErrors` clears field-level and general profile form error messages; `validateForm` validates profile form values and reports any field-level errors; `openModal` opens the profile modal dialog; `closeModal` closes the profile modal dialog.
