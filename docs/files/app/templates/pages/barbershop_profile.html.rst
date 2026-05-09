barbershop_profile.html - Barbershop Profile Page Template
=========================================================

**Purpose**: Display barbershop/salon profile with staff and details.

**What it contains**:

- Shop header with photo/logo
- Shop name and location
- Opening hours and status (open/closed)
- Rating and review count
- Staff/barber list (clickable cards)
- Shop photo gallery
- Embedded map with location
- Customer reviews section
- Contact information
- Services offered
- Website link

**How it works**:

Showcases a barbershop with its location, staff members, portfolio, schedule, reviews, and contact methods. Customers can see the shop, its staff, work samples, and book appointments.

**Key Sections**:

1. **Header**: Shop photo, name, hours, rating
2. **Staff**: Barber cards (clickable to view profiles)
3. **Gallery**: Shop and work photos
4. **Map**: Embedded map showing location
5. **Info**: Address, phone, website, hours
6. **Reviews**: Customer feedback
7. **Services**: List of offered services

**User Interactions**:

- Click staff member to view profile
- Click gallery photo to expand
- View map/directions
- Call shop
- Visit website
- Read reviews
- Share shop profile

**Features**:

- Shop information display
- Staff member cards
- Photo gallery
- Interactive map
- Schedule table
- Review ratings
- Contact buttons
- Share functionality

**Mobile Responsive**:

- Single column layout
- Staff cards stack vertically
- Map full width
- Sticky contact buttons
- Touch-friendly navigation=====

Overview
--------

app/templates/pages/barbershop_profile.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It composes display sections for content rendering and component mounting points used by client scripts. Client behavior is attached through script includes such as leaflet.js and template-resolved JavaScript assets, which connect this template to JavaScript page logic.

Purpose
-------

This template renders the barbershop profile view for the web application. It extends base.html to inherit shared layout and asset structure.
