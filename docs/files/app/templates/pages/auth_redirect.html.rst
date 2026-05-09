auth_redirect.html - Authentication Redirect Page Template
=========================================================

**Purpose**: Intermediate page that handles OAuth/Supabase redirects during authentication.

**What it contains**:

- Loading spinner/animation
- Status message
- Hidden redirect logic (JavaScript)
- Token handling code
- Error message display area
- Fallback redirect button

**How it works**:

After user completes OAuth authentication (or email verification), Supabase redirects them to this page. The page:

1. Extracts authentication token from URL
2. Validates the token
3. Stores token in session/storage
4. Displays loading message
5. Redirects to app dashboard

**User Experience**:

- User sees loading spinner
- Brief pause while token is processed
- Auto-redirected to dashboard
- If error, shows error message

**Behind the Scenes**:

- Captures URL fragment (``#access_token=...``)
- Validates token format
- Stores in session or localStorage
- Links auth user to app user account
- Performs redirect

**Error Handling**:

- Invalid token → show error
- Token expired → show error, link to login
- Network error → show retry button
- Missing token → show error message

**Security**:

- Validates token
- Checks token signature
- Checks token expiration
- Handles untrusted redirects

**Hidden from User**:

- All in JavaScript
- No visible form
- Just a loading page

Overview
--------

app/templates/pages/auth_redirect.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It composes display sections for content rendering and component mounting points used by client scripts. Client behavior is attached through script includes such as supabase-js@2, which connect this template to JavaScript page logic.

Purpose
-------

This template renders the auth redirect view for the web application.
