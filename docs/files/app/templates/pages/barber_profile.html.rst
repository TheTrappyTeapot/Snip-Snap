barber_profile.html - Barber Profile Page Template
=================================================

**Purpose**: Display individual barber's profile with portfolio and reviews.

**What it contains**:

- Barber profile header (photo, name, rating)
- Bio/description
- Follow button
- Gallery/portfolio of work
- Working hours and schedule
- Customer reviews section
- Contact information
- Social media links
- Booking/appointment button
- Share profile option

**How it works**:

Showcases a barber's profile with their photo, bio, portfolio, schedule, and customer reviews. Customers can see their work, ratings, hours, and follow them.

**Key Sections**:

1. **Header**: Photo, name, rating, follow button
2. **Bio**: Description and location
3. **Gallery**: Portfolio photos in grid
4. **Schedule**: Working hours table
5. **Reviews**: Customer feedback with ratings
6. **Contact**: Phone, email, social links

**User Interactions**:

- Click follow button
- Click gallery photo to view full
- Click to book appointment
- Read reviews
- Click share to social media
- Contact barber
- View on map

**Features**:

- Large profile image
- High-quality portfolio display
- Schedule visibility
- Review ratings and text
- Call/message buttons
- Follow button toggle
- Share options
- Responsive layout

**Mobile Responsive**:

- Single column layout
- Large touch targets
- Sticky follow button
- Expandable sections=====

Overview
--------

app/templates/pages/barber_profile.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It composes display sections for content rendering and component mounting points used by client scripts. Client behavior is attached through script includes such as leaflet.js and template-resolved JavaScript assets, which connect this template to JavaScript page logic.

Purpose
-------

This template renders the barber profile view for the web application. It extends base.html to inherit shared layout and asset structure.
