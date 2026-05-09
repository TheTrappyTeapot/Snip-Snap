profile.css - User Profile Page Styles
====================================

**Purpose**: Styling for customer user profile pages.

**What it styles**:

- User profile header
- Profile information section
- Saved/favorite posts
- Followed barbers list
- Edit profile modal/form
- Account settings
- Preferences
- Activity history

**How to use**:

Include in CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/pages/profile.css') }}">

**Page Layout**::

    - Header: User photo, name, follower count
    - Info: Email, location, joined date
    - Tabs: Favorites, Following, Activity
    - Edit Button: Modify profile
    - Settings: Account preferences

**Key Sections**:

- ``.profile-header``: User info section
- ``.profile-tabs``: Tab navigation
- ``.profile-content``: Tab content
- ``.edit-profile-form``: Profile editing
- ``.saved-posts``: Favorite gallery posts
- ``.following-list``: Followed barbers

**Features**:

- User avatar/photo
- Stats (followers, following, saves)
- Tabbed view
- Edit profile button
- Favorite posts display
- Following list

app/static/css/pages/profile.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. It includes 4 media query block(s) to adapt the interface across viewport sizes. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the profile page. It styles selectors such as .profile-page, .profile-card, .profile-card__header, and .profile-card__title.
