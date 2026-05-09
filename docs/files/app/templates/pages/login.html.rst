login.html - Login Page Template
===============================

**Purpose**: User login page interface.

**What it contains**:

- Email input field
- Password input field
- Login button
- "Remember me" checkbox
- Link to signup page
- Password reset link
- Form validation messages
- Loading spinner during submission

**How it works**:

Users enter their email and password, then click login. The ``login.js`` script handles validation and sends credentials to Supabase for authentication. On success, user is logged in and redirected to dashboard.

**User Flow**:

1. User enters email address
2. User enters password
3. (Optional) Check "Remember me"
4. Click Login button
5. Form validates input locally
6. Submits to authentication API
7. On success: redirects to dashboard
8. On error: shows error message

**Links**:

- Don't have account? → ``/signup``
- Forgot password? → ``/password-reset``

**Responsive Design**:

- Mobile: Full-width form
- Desktop: Centered login card
- Touch-friendly input fields

**Security Features**:

- CSRF token in form
- Password input masked
- No credential storage
- Secure session cookies=

Overview
--------

app/templates/pages/login.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It contains 1 form(s) that collect user input and submit data through frontend scripts or route handlers. Client behavior is attached through script includes such as supabase-js@2 and template-resolved JavaScript assets, which connect this template to JavaScript page logic.

Purpose
-------

This template renders the login view for the web application. It extends base.html to inherit shared layout and asset structure.
