taglist.html - Tags/Categories Display Template
==============================================

**Purpose**: Display list of available tags/categories for haircut styles and filtering.

**What it contains**:

- Tag/category list display
- Clickable tag chips
- Count of items per tag (optional)
- Search/filter tags
- Tag categories/groups
- Visual styling for tag types
- Responsive wrapping

**How it works**:

Shows available haircut style tags that users can click to filter gallery or barber posts. Tags are displayed as chips/buttons that users can interact with.

**Tag Examples**:

- **Fade**: Fade haircut
- **Undercut**: Undercut style
- **Buzz**: Buzz cut
- **Modern**: Modern style
- **Classic**: Classic cuts
- **Mohawk**: Mohawk style
- **Temp Fade**: Temp fade cut
- **Line Design**: Line design/art

**How Users Interact**:

1. See list of available tags
2. Click tag to filter
3. Gallery updates to show only tagged items
4. Click again to remove filter
5. Multiple tags can be selected (OR filter)

**Visual Design**:

- Chips/buttons for tags
- Color coding (optional)
- Icons (optional)
- Count badges
- Hover effects
- Click feedback

**Mobile Responsive**:

- Tags wrap on small screens
- Touch-friendly size
- Horizontal scroll option
- Bottom navigation integration

**Features**:

- Click to filter
- Multiple selection
- Search within tags
- Popular tags highlight
- Tag count display
- Category grouping
- Dark mode support==

Overview
--------

app/templates/pages/taglist.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It composes display sections for content rendering and component mounting points used by client scripts. Client behavior is attached through script includes such as TagList.js, which connect this template to JavaScript page logic.

Purpose
-------

This template renders the taglist view for the web application.
