discoverSearch.js - Discovery Search Feature
============================================

**Purpose**: Implements search and filtering on the discovery/gallery page.

**What it does**:

- Provides real-time search through gallery posts
- Implements filters (by barber, location, style, rating)
- Handles pagination for large result sets
- Updates UI with search results
- Manages search history/saved searches
- Auto-suggest based on popular searches

**How to use**:

Include in page::

    <script src="{{ url_for('static', filename='js/features/discoverSearch.js') }}"></script>

HTML structure::

    <div class="discover-search">
        <input type="text" id="searchInput" placeholder="Search haircuts..." />
        <div id="filters"></div>
        <div id="results"></div>
    </div>

**Key Functions**:

- ``DiscoverSearch(container)``: Initialize search
- ``search(query)``: Perform search query
- ``filter(criteria)``: Apply filters
- ``paginate(page)``: Load next page of results
- ``getPopularSearches()``: Get trending searches

**API Endpoints**:

- ``GET /api/discover?q=<query>``: Search posts
- ``GET /api/discover?filter=<filter>&value=<value>``: Filter results
- ``GET /api/discover?page=<page>&limit=20``: Pagination

**Filters**:

- By barber name
- By location/postcode
- By haircut style
- By rating
- By date (recent first)

**Features**:

- Live search as you type
- Multiple simultaneous filters
- Saved favorites
- Search suggestions
- Results pagination

The script in app/static/js/features/discoverSearch.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/discover/search_items to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/features/discoverSearch.js` provides frontend browser behavior. Function responsibilities: `dedupeAdd` deduplicates add; `onSelect` returns on select.