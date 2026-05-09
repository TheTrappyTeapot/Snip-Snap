signup.html - User Registration Page Template
============================================

**Purpose**: User account registration/signup page.

**What it contains**:

- Email input field
- Password input with strength indicator
- Confirm password field
- Username input
- Role selection (customer/barber) - radio buttons or toggle
- Terms of service checkbox
- Signup button
- Link to login page
- Form validation messages
- Loading spinner during submission

**How it works**:

New users enter their information and select their role. The form is validated client-side, then submitted to create a new account via Supabase.

**User Flow**:

1. User enters email
2. User creates password (with strength requirements)
3. User confirms password
4. User enters username
5. User selects role (customer or barber)
6. User agrees to terms
7. Click signup
8. Account created
9. Redirected to login or verification page

**Password Requirements**:

- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character

**Role Selection**:

- **Customer**: Browse and rate haircuts
- **Barber**: Upload portfolio and manage bookings

**Responsive Design**:

- Mobile: Full-width form
- Desktop: Centered signup card
- Touch-friendly inputs

**Security Features**:

- Password strength meter
- CSRF token in form
- Password input masked
- Terms acceptance required=

Overview
--------

app/templates/pages/signup.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It contains 1 form(s) that collect user input and submit data through frontend scripts or route handlers. Client behavior is attached through script includes such as supabase-js@2 and template-resolved JavaScript assets, which connect this template to JavaScript page logic.

Purpose
-------

This template renders the signup view for the web application. It extends base.html to inherit shared layout and asset structure.
