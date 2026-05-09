barber_profile.css - Barber Profile Page Styles
==============================================

**Purpose**: Specific styling for individual barber profile pages.

**What it styles**:

- Page header with barber photo and info
- Rating and review section
- Gallery/portfolio grid
- Timetable/working hours
- Contact information
- Social media links
- Review list
- Follow/booking buttons

**How to use**:

Include page-specific CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/pages/barber_profile.css') }}">

**Page Layout**::

    - Header: Barber photo, name, rating, follow button
    - Info Section: Bio, location, contact
    - Gallery: Portfolio of haircuts
    - Schedule: Working hours and availability
    - Reviews: Customer feedback

**Key Sections**:

- ``.barber-header``: Top section with profile
- ``.barber-info``: Bio and contact
- ``.barber-gallery``: Portfolio photos
- ``.barber-schedule``: Working hours
- ``.barber-reviews``: Customer reviews
- ``.barber-actions``: Buttons (follow, book)

**Responsive Design**:

- Mobile: Stacked layout
- Tablet: 2-column layout
- Desktop: Multi-column with sidebar

**Features**:

- Large profile image
- Quick booking access
- Photo gallery scrollable
- Schedule visible inline
- Review ratings display

app/static/css/pages/barber_profile.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. It includes 1 media query block(s) to adapt the interface across viewport sizes. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the barber profile page. It styles selectors such as .barber-profile-container, .barber-profile__header, .barber-profile__info-section, and .barber-profile__info-grid.
