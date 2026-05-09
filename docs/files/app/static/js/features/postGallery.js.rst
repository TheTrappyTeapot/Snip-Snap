postGallery.js - Gallery Post Browsing Feature
============================================

**Purpose**: Core feature for browsing and interacting with gallery posts.

**What it does**:

- Loads posts from API
- Renders posts to gallery grid
- Handles infinite scroll or pagination
- Manages like/unlike interactions
- Manages follow/unfollow barbers
- Handles post filtering
- Tracks user interactions
- Manages loading/error states

**How to use**:

Initialize feature::

    const gallery = new PostGalleryFeature('galleryContainer');
    gallery.load();
    gallery.setFilter({ location: 'London', style: 'Fade' });

**Key Functions**:

- ``PostGalleryFeature(container)``: Initialize
- ``load()``: Fetch initial posts
- ``loadMore()``: Load next page
- ``setFilter(criteria)``: Apply filters
- ``likePost(postId)``: Like photo
- ``unlikePost(postId)``: Unlike photo
- ``followBarber(barberId)``: Follow barber
- ``unfollowBarber(barberId)``: Unfollow barber

**API Endpoints**:

- ``GET /api/discover```: Get posts
- ``POST /api/post/<id>/like``: Like
- ``DELETE /api/post/<id>/like``: Unlike
- ``POST /api/follow``: Follow barber

**Features**:

- Infinite scroll
- Filter and search
- Like/unlike
- Follow/unfollow
- Open post details
- Share posts
- View barber profile

The script in app/static/js/features/postGallery.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/gallery/posts to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/features/postGallery.js` provides frontend browser behavior. Function responsibilities: `normaliseTagListItems` groups selected tag-list entries into filter/tag/barber/barbershop ID arrays; `resolveEffectiveSort` determines whether sorting should be `most_recent`, `closest`, `highest_rated`, or blended based on active filters; `createGalleryLoader` creates the loading indicator element shown while requests are in flight; `setLoadingVisible` toggles loader visibility for fetch states; `render` draws either empty/error states or the gallery grid for current items; `buildPayload` assembles the API request body from current filter state and pagination cursor; `payloadKey` builds a stable serialized key used to detect filter-state changes across page loads.
