dashboard.html - Barber Dashboard Page Template
============================================

**Purpose**: Management dashboard for barbers to manage their profile and business.

**What it contains**:

- Navigation sidebar with menu items
- Dashboard header with user info
- Statistics cards (views, followers, rating)
- Tab sections:
  - Profile editing form
  - Gallery upload and management
  - Schedule/hours editor
  - Reviews section
  - Analytics/statistics
- Save/Cancel buttons for each section
- Loading indicators
- Success/error messages

**How it works**:

Barbers log into their dashboard to manage their profile, portfolio, schedule, and view their reviews and statistics. They can edit all their business information from one place.

**Dashboard Tabs**:

1. **Profile**: Edit photo, name, bio, contact info
2. **Gallery**: Upload/manage/reorder photos
3. **Schedule**: Set working hours and breaks
4. **Reviews**: View customer feedback
5. **Analytics**: View statistics (views, followers, ratings)
6. **Settings**: Account and business preferences

**Key Features**:

- Tabbed interface
- Real-time stats
- Photo upload
- Schedule editor
- Review management
- Analytics dashboard
- Form validation
- Auto-save functionality
- Mobile-friendly

**Sections**:

- **Stats**: Key metrics at top
- **Forms**: Edit sections in tabs
- **Preview**: See how public profile looks
- **History**: Recent activity log

**Mobile Responsive**:

- Sidebar collapses to hamburger
- Full-width tabs
- Mobile-optimized forms
- Bottom navigation option=

Overview
--------

app/templates/pages/dashboard.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It contains 4 form(s) that collect user input and submit data through frontend scripts or route handlers. Client behavior is attached through script includes such as template-resolved JavaScript assets, template-resolved JavaScript assets, and template-resolved JavaScript assets, which connect this template to JavaScript page logic.

Purpose
-------

This template renders the dashboard view for the web application. It extends base.html to inherit shared layout and asset structure.
