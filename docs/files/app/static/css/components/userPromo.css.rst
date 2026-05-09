userPromo.css - User Profile Promo Card Styles
==============================================

**Purpose**: Styles for user profile promotional cards on barber pages.

**What it styles**:

- Profile card container
- Profile photo display
- Bio/description text
- Rating and review count
- Follow button
- Contact information
- Social media links
- Background and decorative elements

**How to use**:

Include in CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/userPromo.css') }}">

HTML structure::

    <div class="user-promo">
        <img src="profile.jpg" class="user-promo-photo" />
        <h2 class="user-promo-name">John Barber</h2>
        <p class="user-promo-bio">Professional barber with 5 years experience</p>
        <div class="user-promo-rating">⭐ 4.9 (125 reviews)</div>
        <button class="btn-follow">Follow</button>
    </div>

**Key CSS Classes**:

- ``.user-promo``: Card container
- ``.user-promo-photo``: Profile picture
- ``.user-promo-name``: Name heading
- ``.user-promo-bio``: Bio/description
- ``.user-promo-rating``: Ratings
- ``.btn-follow``: Follow button

**Features**:

- Large profile image
- Prominent call-to-action
- Social proof (ratings)
- Contact methods
- Following status toggle
- Mobile-friendly layout

app/static/css/components/userPromo.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. Its rules provide the base visual treatment used when rendering the related template/components. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the userPromo component. It styles selectors such as .user-promo, .user-promo__avatar, .user-promo__avatar img, and .user-promo__text.
