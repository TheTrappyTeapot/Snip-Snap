barbershop_profile.css - Barbershop Profile Page Styles
=====================================================

**Purpose**: Styling for barbershop/salon profile pages.

**What it styles**:

- Shop header with logo/photo
- Shop name and location
- Rating and review count
- Opening hours and status
- Staff/barber list
- Gallery of work
- Services offered
- Contact information
- Map/directions

**How to use**:

Include in CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/pages/barbershop_profile.css') }}">

**Page Layout**::

    - Header: Shop photo, name, location, rating
    - Status: Open/closed, hours
    - Staff: Barbers working here
    - Gallery: Shop and work photos
    - Info: Address, phone, website
    - Map: Location on map
    - Reviews: Customer feedback

**Key Sections**:

- ``.shop-header``: Header section
- ``.shop-info``: Contact and details
- ``.shop-status``: Open/closed status
- ``.shop-staff``: Staff barber list
- ``.shop-gallery``: Photos grid
- ``.shop-location``: Address and map

**Features**:

- Large shop image
- Staff member cards (clickable)
- Gallery grid
- Embedded map
- Hours and status
- Contact buttons

app/static/css/pages/barbershop_profile.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. It includes 1 media query block(s) to adapt the interface across viewport sizes. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the barbershop profile page. It styles selectors such as .barbershop-container, .barbershop__header, .barbershop__name, and .barbershop__info-grid.
