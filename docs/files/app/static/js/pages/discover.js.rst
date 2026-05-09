discover.js - Discovery Page Script
==================================

**Purpose**: Manages the gallery discovery and browsing experience.

**What it does**:

- Loads gallery posts from API
- Implements infinite scroll or pagination
- Handles post filtering and search
- Manages like/favorite functionality
- Shows barber details on click
- Tracks user interactions
- Manages loading states

**How to use**:

Include in discover page::

    <script src="{{ url_for('static', filename='js/pages/discover.js') }}"></script>

**Key Functions**:

- ``DiscoveryPage(container)``: Initialize page
- ``loadPosts(page, filter)``: Fetch posts from API
- ``renderPost(postData)``: Display individual post
- ``infiniteScroll()``: Auto-load more on scroll
- ``likePost(postId)``: Like a photo
- ``filterPosts(criteria)``: Apply filters

**API Endpoints**:

- ``GET /api/discover?page=<page>``: Get paginated posts
- ``GET /api/discover?filter=<filter>``: Filter posts
- ``POST /api/post/<id>/like``: Like a post
- ``GET /api/barber/<id>``: Get barber details

**Features**:

- Infinite scroll loading
- Like/favorite posts
- Share options
- Filter by location, style, rating
- Click to view barber profile
- View full image modal
- Comment on photos
- Follow barber from card

**UI Elements**:

- Gallery grid layout
- Post cards with image, barber info, rating
- Filter sidebar
- Like button and count
- "Follow" button
- Barber name and location
- Rating stars

The script in app/static/js/pages/discover.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/discover/search_items and /api/gallery/posts to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/pages/discover.js` provides frontend browser behavior.