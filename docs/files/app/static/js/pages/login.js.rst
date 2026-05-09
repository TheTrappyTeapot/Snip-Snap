login.js - Login Page Script
===========================

**Purpose**: Handles user login form and authentication.

**What it does**:

- Manages login form submission
- Validates email and password input
- Sends credentials to Supabase authentication
- Handles authentication errors
- Stores JWT token in session/local storage
- Redirects to dashboard after successful login
- Shows "Remember me" functionality

**How to use**:

Include in login page::

    <script src="{{ url_for('static', filename='js/pages/login.js') }}"></script>

HTML form::

    <form id="loginForm">
        <input type="email" name="email" placeholder="Email" required />
        <input type="password" name="password" placeholder="Password" required />
        <button type="submit">Login</button>
    </form>

**Key Functions**:

- ``handleLogin(email, password)``: Authenticate user
- ``validateEmail(email)``: Validate email format
- ``validatePassword(password)``: Check password
- ``storeToken(token)``: Save authentication token
- ``redirectToDashboard()``: Navigate to app

**API Endpoint**:

``POST /api/auth/login`` - Authenticate user

**Features**:

- Email/password authentication
- Remember me checkbox
- Error message display
- Loading state during auth
- Link to signup page
- Link to password reset
- Redirect to referrer after login

**Error Handling**:

- Invalid email format
- Wrong password
- Account not found
- Account disabled
- Rate limiting

The script in app/static/js/pages/login.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/pages/login.js` provides frontend browser behavior. Function responsibilities: `clearErrors` clears errors; `validateForm` validates form.