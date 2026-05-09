review_widget.css - Review Widget Component Styles
==================================================

**Purpose**: Styles for displaying customer reviews and ratings.

**What it styles**:

- Review card layout and container
- Star rating display
- Review text and author information
- Helpful vote buttons
- Review form for submitting new reviews
- Rating input component

**How to use**:

Include in CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/review_widget.css') }}">

HTML structure::

    <div class="review-widget">
        <div class="review-card">
            <div class="review-rating">
                <span class="stars">★★★★★</span>
                <span class="rating-value">5.0</span>
            </div>
            <p class="review-text">Great service!</p>
            <p class="review-author">By John D.</p>
            <button class="helpful-btn">Helpful (5)</button>
        </div>
    </div>

**Key CSS Classes**:

- ``.review-widget``: Main container
- ``.review-card``: Individual review
- ``.review-rating``: Rating display
- ``.stars``: Star rating visuals
- ``.review-text``: Review content
- ``.helpful-btn``: Helpful vote button
- ``.review-form``: Review submission form

**Features**:

- 1-5 star rating display
- Helpful vote tracking
- Review filtering by rating
- Responsive card layout
- Form validation for new reviews

app/static/css/components/review_widget.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. Its rules provide the base visual treatment used when rendering the related template/components. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the review widget component. It styles selectors such as .widget-container, .widget-header, .add-review-btn, and .review-list.
