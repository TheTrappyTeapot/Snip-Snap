postImageCard.css - Post Image Card Styles
==========================================

**Purpose**: Styles for individual photo post cards in galleries and feeds.

**What it styles**:

- Card container and layout
- Image display and aspect ratio
- Card content area (caption, metadata)
- Overlay on hover
- Action buttons (like, share, etc.)
- User/barber info section
- Rating display

**How to use**:

Include in CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/postImageCard.css') }}">

HTML structure::

    <div class="post-card">
        <img src="photo.jpg" class="post-image" />
        <div class="post-overlay">
            <button class="btn-like">❤</button>
        </div>
        <div class="post-content">
            <h3 class="barber-name">John's Cuts</h3>
            <p class="post-caption">Classic fade</p>
            <div class="post-rating">⭐ 4.8</div>
        </div>
    </div>

**Key CSS Classes**:

- ``.post-card``: Main card container
- ``.post-image``: Photo image
- ``.post-overlay``: Hover overlay
- ``.post-content``: Caption/info area
- ``.post-rating``: Rating display
- ``.btn-like``: Like button

**Features**:

- Hover effects
- Action buttons overlay
- Responsive card sizing
- Caption truncation
- Like count display
- User info accessible

app/static/css/components/postImageCard.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. It includes 2 media query block(s) to adapt the interface across viewport sizes. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the postImageCard component. It styles selectors such as .postImageCard, .postImageCard:hover, .postImageCard__media, and .postImageCard__img.
