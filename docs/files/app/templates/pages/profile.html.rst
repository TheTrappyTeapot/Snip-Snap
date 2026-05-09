profile.html - User Profile Page Template
=========================================

**Purpose**: Display user's profile page with account information.

**What it contains**:

- User profile header with photo
- User stats (followers, following, saved posts)
- Tab navigation (Favorites, Following, Activity, Settings)
- Saved/favorite gallery posts grid
- Followed barbers list
- Activity history timeline
- Edit profile button
- Settings section
- Logout button

**How it works**:

Displays the current user's profile with their information, saved content, and account settings. Users can edit profile, view favorites, manage follows, and access account settings.

**Key Sections**:

1. **Header**: Profile photo, name, follower stats
2. **Tabs**: Navigation between sections
3. **Favorites Tab**: Grid of saved gallery posts
4. **Following Tab**: List of followed barbers
5. **Activity Tab**: Recent user actions
6. **Settings Tab**: Account preferences

**User Interactions**:

- Click profile photo to edit
- Click tab to switch section
- Click favorite post to view full
- Click followed barber to go to profile
- Click "Edit Profile" button
- Click "Settings" for account options
- Click "Logout" to sign out

**Features**:

- Responsive tabs
- Infinite scroll in tabs
- Search within sections
- Edit profile modal
- Settings modal
- Dark/light theme toggle

**Mobile Responsive**:

- Stacked layout
- Touch-friendly tabs
- Full-width sections
- Bottom navigation on mobile==

Overview
--------

app/templates/pages/profile.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It contains 2 form(s) that collect user input and submit data through frontend scripts or route handlers. Client behavior is attached through script includes such as template-resolved JavaScript assets, template-resolved JavaScript assets, and template-resolved JavaScript assets, which connect this template to JavaScript page logic.

Purpose
-------

This template renders the profile view for the web application. It extends base.html to inherit shared layout and asset structure.
