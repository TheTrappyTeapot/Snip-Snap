welcome.html - Welcome/Landing Page Template
=========================================

**Purpose**: Welcome page shown to users before login or on app launch.

**What it contains**:

- Welcome message/header
- Brief app description
- Key features highlighted
- Call-to-action buttons (Sign Up, Login)
- Featured content/screenshots
- Navigation to pages
- Footer with links
- Hero image/banner

**How it works**:

First page users see when visiting the app. Shows what the app is about, highlights key features, and guides users to login or signup.

**Page Sections**:

1. **Hero**: Welcome title and tagline
2. **Features**: 3-4 key benefits
3. **Call-to-Action**: Login/Signup buttons
4. **Screenshots**: App interface preview
5. **Footer**: Links, social, info

**Content**:

**Hero Section**:
- "Discover Your Perfect Barber"
- App tagline
- Large signup button

**Features**:
- Browse haircuts
- Find barbers nearby
- Book appointments
- Leave reviews

**Call-to-Action Buttons**:
- "Get Started" → Signup
- "Sign In" → Login

**User Flow**:

1. User visits app
2. Sees welcome page
3. Reads features
4. Clicks Sign Up or Login
5. Goes to authentication page

**Design**:

- Large hero image
- Clean layout
- Mobile responsive
- High contrast CTAs
- Feature icons
- Testimonials (optional)

**Mobile Responsive**:

- Single column
- Full-width buttons
- Stacked sections
- Touch-friendly
- Vertical scrolling===

Overview
--------

app/templates/pages/welcome.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It contains 1 form(s) that collect user input and submit data through frontend scripts or route handlers. Named template blocks such as title, page_title, styles, and content allow base layout integration and page-specific content injection.

Purpose
-------

This template renders the welcome view for the web application. It extends base.html to inherit shared layout and asset structure.
