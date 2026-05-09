app/input_sanitization.py - Input Validation and Sanitization
==============================================================

**Purpose**: Validates and sanitizes user input to prevent security vulnerabilities and ensure data quality.

**What it does**:

This module provides validation functions for all user inputs. It prevents:

- SQL injection through input sanitization
- Invalid email formats
- Weak passwords
- Invalid usernames
- Oversized text fields
- Special character misuse

**Key Functions**:

- ``sanitize_input(text, max_length)``: Removes dangerous characters
- ``validate_email(email)``: Validates email format
- ``validate_password(password)``: Checks password strength
- ``validate_username(username)``: Validates username format
- ``validate_postcode(postcode)``: Validates UK postcode format
- ``validate_rating(rating)``: Validates review rating (1-5)
- ``validate_review_text(text)``: Validates review text length and content

**How to use**:

Call validation functions before processing user input::

    from app.input_sanitization import validate_email, validate_password
    
    try:
        email = validate_email(user_input_email)
        password = validate_password(user_input_password)
    except ValueError as e:
        return {"error": str(e)}, 400  # Return validation error

**Validation Rules**:

- **Email**: Must match standard email pattern
- **Password**: Minimum 8 characters, at least 1 uppercase, 1 lowercase, 1 number, 1 special char
- **Username**: 3-20 alphanumeric characters, underscores allowed
- **Postcode**: Valid UK postcode format (e.g., SW1A1AA)
- **Rating**: Integer between 1 and 5

**Security Benefits**:

- Prevents injection attacks
- Protects against XSS vulnerabilities
- Ensures consistent data format
- Provides user-friendly error messages

Overview
--------

It normalizes and cleans input to reduce malformed values before database writes and template rendering. Route and API handlers call sanitize_input when accepting profile and review content. Keeping sanitization in one helper avoids inconsistent validation behavior across endpoints.

Purpose
-------

This module in `app/input_sanitization.py` provides backend application behavior. Function responsibilities: `sanitize_input` validate a user-supplied string.