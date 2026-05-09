userPromo.js - User Profile Promo Card Component
===============================================

**Purpose**: Display user/barber profile promotional card.

**What it does**:

- Renders profile card with photo and info
- Shows ratings and review count
- Displays follow/unfollow button
- Shows social metrics (followers, etc.)
- Handles follow/unfollow interactions
- Manages click to view full profile
- Shows contact information

**How to use**:

Include in page::

    <script src="{{ url_for('static', filename='js/components/userPromo.js') }}"></script>

Display user card::

    const promo = new UserPromo(userData, container);
    promo.render();
    promo.onFollow(() => updateFollowStatus());
    promo.onProfileClick(() => navigateToProfile());

**Key Functions**:

- ``UserPromo(data, container)``: Initialize
- ``render()``: Display card
- ``follow()``: Follow user
- ``unfollow()``: Unfollow user
- ``updateInfo(data)``: Refresh data
- ``showDetails()``: Open profile view

**Features**:

- Large profile photo
- Name and bio
- Rating stars and count
- Follower count
- Follow/Unfollow button
- Click to navigate
- Social links
- Contact buttons

The script in app/static/js/components/userPromo.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/userPromo.js` provides frontend browser behavior.