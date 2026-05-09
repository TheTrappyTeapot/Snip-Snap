signup.js - Signup Page Script
=============================

**Purpose**: Handles user registration and account creation.

**What it does**:

- Manages signup form
- Validates all input fields
- Sends registration to Supabase
- Handles email verification
- Manages role selection (customer/barber)
- Shows validation errors
- Handles success and redirects
- Manages loading states

**How to use**:

Include in signup page::

    <script src="{{ url_for('static', filename='js/pages/signup.js') }}"></script>

**Key Functions**:

- ``handleSignup(formData)``: Process registration
- ``validateEmail(email)``: Check email
- ``validatePassword(password)``: Check strength
- ``validateUsername(username)``: Check availability
- ``selectRole(role)``: Choose role
- ``submitForm()``: Create account
- ``resendVerification()``: Resend email

**Form Fields**:

- Email
- Password (with strength indicator)
- Confirm password
- Username
- Role (customer or barber)
- Terms of service checkbox

**API Endpoints**:

- ``POST /api/auth/signup``: Create account
- ``POST /api/auth/send-verification``: Send email

**Validation**:

- Valid email format
- Password min 8 characters
- Password strength requirements
- Username uniqueness
- Terms acceptance

**Features**:

- Form validation
- Password strength meter
- Role selection
- Email verification
- Error messages
- Success redirect
- Link to login page

The script in app/static/js/pages/signup.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/auth/create-user to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/pages/signup.js` provides frontend browser behavior. Function responsibilities: `initializeForm` initializes the signup form when the DOM is ready; `clearErrors` clears visible validation and general error messages; `validateForm` validates signup inputs and returns true when the form is valid.
