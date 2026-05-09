discover.html - Discovery Gallery Page Template
==============================================

**Purpose**: Main page for browsing and discovering haircut photos and barbers.

**What it contains**:

- Search bar
- Filter options (location, style, rating)
- Gallery grid of haircut photos
- Infinite scroll or "Load More" button
- Post cards with barber info
- Like button
- Follow button
- Share options

**How it works**:

Page loads initial gallery posts and displays them in a responsive grid. As user scrolls, more posts are automatically loaded. Users can search, filter, like photos, and follow barbers from this page.

**Key Sections**:

1. **Header**: Logo, search, user menu
2. **Filter Sidebar**: Location, style, rating filters
3. **Gallery Grid**: Posts displayed in responsive columns
4. **Post Card**: Photo, barber name, location, rating, like count, follow button

**User Interactions**:

- **Search**: Type to find haircuts
- **Filter**: Select criteria to narrow results
- **Like**: Click heart icon to save favorite
- **Follow**: Click to follow barber
- **Click Photo**: View full size and details
- **Click Barber Name**: Go to barber profile

**Responsive Grid**:

- Mobile: 1-2 columns
- Tablet: 2-3 columns
- Desktop: 3-4 columns

**Features**:

- Real-time filtering
- Infinite scroll auto-load
- Favorites/saved posts
- Share to social media
- View barber profile
- Leave comments
- Submit reviews==

Overview
--------

app/templates/pages/discover.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It composes display sections for content rendering and component mounting points used by client scripts. Client behavior is attached through script includes such as template-resolved JavaScript assets and template-resolved JavaScript assets, which connect this template to JavaScript page logic.

Purpose
-------

This template renders the discover view for the web application. It extends base.html to inherit shared layout and asset structure.
