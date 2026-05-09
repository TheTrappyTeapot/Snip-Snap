review_widget.js - Review Display Widget Component
=================================================

**Purpose**: Display and manage customer reviews and ratings.

**What it does**:

- Renders reviews list
- Shows star ratings
- Manages helpful votes
- Handles review form submission
- Filters reviews by rating
- Manages pagination
- Shows review replies

**How to use**:

Include in page::

    <script src="{{ url_for('static', filename='js/components/review_widget.js') }}"></script>

Initialize widget::

    const reviews = new ReviewWidget('reviewsContainer', barberId);
    reviews.load();
    reviews.allowSubmit(true);

**Key Functions**:

- ``ReviewWidget(container, barberId)``: Initialize
- ``load()``: Fetch reviews from API
- ``render()``: Display reviews
- ``submitReview(rating, text)``: Add new review
- ``toggleHelpful(reviewId)``: Mark as helpful
- ``filterByRating(rating)``: Show only N-star reviews
- ``paginate(page)``: Load more reviews

**API Endpoints**:

- ``GET /api/reviews/<barber_id>``: Get reviews
- ``POST /api/reviews``: Submit review
- ``POST /api/reviews/<id>/helpful``: Mark helpful

**Features**:

- Star ratings display
- Helpful vote counter
- Review form
- Pagination
- Filter by rating
- Author info
- Date display
- Reply to reviews

The script in app/static/js/components/review_widget.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/review_widget.js` provides frontend browser behavior.