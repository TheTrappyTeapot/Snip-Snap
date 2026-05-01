"""
input_sanitization.py

Provides sanitize_input(text) — call this before saving any user-supplied
string (usernames, bios, reviews, etc.) to the database.

Returns:
    None      — input is clean, safe to use
    str       — human-readable error message explaining the problem
"""

import re

# Basic profanity list (lowercase, extend as needed)
_PROFANITIES = {
    "shit", "fuck", "bitch", "asshole", "bastard", "cunt", "dick",
    "prick", "twat", "wanker", "arse", "bollocks", "cock", "pussy",
    "slut", "whore", "nigger", "nigga", "faggot", "fag", "retard",
    "damn", "crap", "piss", "ass",
}


def sanitize_input(text):
    """
    Validate a user-supplied string.

    Checks performed (in order):
      1. Not null / not empty after stripping whitespace
      2. No profanities (whole-word match, case-insensitive)

    Args:
        text: The value to check. May be any type; non-strings are rejected.

    Returns:
        None if the input is acceptable.
        A str error message if the input is unacceptable.
    """
    if text is None:
        return "Input must not be empty."

    if not isinstance(text, str):
        return "Input must be a string."

    stripped = text.strip()
    if not stripped:
        return "Input must not be empty."

    # Whole-word profanity check (ignores partial matches like "assassin")
    lowered = stripped.lower()
    words = re.findall(r"[a-z]+", lowered)
    for word in words:
        if word in _PROFANITIES:
            return "Input contains inappropriate language."

    return None


# ============================================================================
# INPUT VALIDATION MODULE
# ============================================================================
# Centralized validation functions for username, email, password, and postcode


def validate_username(username):
    """
    Validate a username.

    Checks performed (in order):
      1. Not null / not empty after stripping whitespace
      2. Between 2 and 50 characters
      3. No profanities (via sanitize_input)

    Args:
        username: The username to validate.

    Returns:
        None if the username is acceptable.
        A str error message if the username is unacceptable.
    """
    if not username or not isinstance(username, str):
        return "Username is required."

    stripped = username.strip()
    if not stripped:
        return "Username is required."

    if len(stripped) < 2:
        return "Username must be at least 2 characters."

    if len(stripped) > 50:
        return "Username must be 50 characters or fewer."

    # Check for profanities
    err = sanitize_input(stripped)
    if err:
        return err

    return None


def validate_email(email):
    """
    Validate an email address.

    Checks performed (in order):
      1. Not null / not empty after stripping whitespace
      2. Valid email format (basic regex)

    Args:
        email: The email address to validate.

    Returns:
        None if the email is acceptable.
        A str error message if the email is unacceptable.
    """
    if not email or not isinstance(email, str):
        return "Email is required."

    stripped = email.strip().lower()
    if not stripped:
        return "Email is required."

    # Basic email regex: something@something.something
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", stripped):
        return "Please enter a valid email address."

    return None


def validate_password(password):
    """
    Validate a password.

    Checks performed (in order):
      1. Not null / not empty
      2. At least 6 characters
      3. At most 50 characters
      4. Contains at least 1 uppercase letter
      5. Contains at least 1 lowercase letter
      6. Contains at least 1 number
      7. Contains at least 1 special character

    Args:
        password: The password to validate.

    Returns:
        None if the password is acceptable.
        A str error message if the password is unacceptable.
    """
    if not password or not isinstance(password, str):
        return "Password is required."

    if len(password) < 6:
        return "Password must be at least 6 characters."

    if len(password) > 50:
        return "Password must be 50 characters or fewer."

    has_uppercase = any(c.isupper() for c in password)
    has_lowercase = any(c.islower() for c in password)
    has_number = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{};\':\"\\|,.<>/?~`" for c in password)

    missing_requirements = []
    if not has_uppercase:
        missing_requirements.append("1 uppercase letter")
    if not has_lowercase:
        missing_requirements.append("1 lowercase letter")
    if not has_number:
        missing_requirements.append("1 number")
    if not has_special:
        missing_requirements.append("1 special character")

    if missing_requirements:
        return "Password must include: " + ", ".join(missing_requirements) + "."

    return None


def validate_postcode(postcode):
    """
    Validate a UK postcode.

    Checks performed (in order):
      1. Not null / not empty after stripping whitespace
      2. At most 8 characters (UK postcode format)
      3. Matches UK postcode format (e.g., "SW1A 1AA", "B33 8TH")
      4. No profanities (via sanitize_input)

    UK Postcode Format:
      - Outward code: 1-2 letters + 1-2 digits (+ optional letter)
      - Inward code: 1 digit + 2 letters
      - Example: SW1A 1AA, B33 8TH, CR2 6XH (space is optional)

    Args:
        postcode: The postcode to validate.

    Returns:
        None if the postcode is acceptable.
        A str error message if the postcode is unacceptable.
    """
    if not postcode or not isinstance(postcode, str):
        return "Postcode is required."

    stripped = postcode.strip().upper()
    if not stripped:
        return "Postcode is required."

    if len(stripped) > 8:
        return "Postcode is too long."

    # UK postcode regex: format is [1-2 letters][1-2 digits][optional letter] [1 digit][2 letters]
    # Examples: SW1A 1AA, B33 8TH, CR2 6XH, M1 1AA
    # Space is optional in the regex but commonly present
    uk_postcode_pattern = r"^[A-Z]{1,2}[0-9]{1,2}[A-Z]?\s?[0-9][A-Z]{2}$"
    
    if not re.match(uk_postcode_pattern, stripped):
        return "Please enter a valid UK postcode (e.g., SW1A 1AA or B33 8TH)."

    # Check for profanities
    err = sanitize_input(stripped)
    if err:
        return err

    return None


def validate_review_text(text):
    """
    Validate review/comment text.

    Checks performed (in order):
      1. Not null / not empty after stripping whitespace
      2. Between 1 and 1000 characters
      3. No profanities (via sanitize_input)

    Args:
        text: The review text to validate.

    Returns:
        None if the text is acceptable.
        A str error message if the text is unacceptable.
    """
    if not text or not isinstance(text, str):
        return "Review text is required."

    stripped = text.strip()
    if not stripped:
        return "Review text is required."

    if len(stripped) > 1000:
        return "Review text must be 1000 characters or fewer."

    # Check for profanities
    err = sanitize_input(stripped)
    if err:
        return err

    return None


def validate_rating(rating):
    """
    Validate a rating value.

    Checks performed (in order):
      1. Is an integer
      2. Between 1 and 5 (inclusive)

    Args:
        rating: The rating to validate (should be an integer from 1-5).

    Returns:
        None if the rating is acceptable.
        A str error message if the rating is unacceptable.
    """
    if rating is None:
        return "Rating is required."

    if not isinstance(rating, int):
        return "Rating must be a number."

    if not (1 <= rating <= 5):
        return "Rating must be between 1 and 5."

    return None


def validate_name(name, max_length=255):
    """
    Validate a display name (for barbershops, profiles, etc.).

    Checks performed (in order):
      1. Not null / not empty after stripping whitespace
      2. Between 1 and max_length characters (default 255)
      3. No profanities (via sanitize_input)

    Args:
        name: The name to validate.
        max_length: Maximum allowed length (default: 255).

    Returns:
        None if the name is acceptable.
        A str error message if the name is unacceptable.
    """
    if not name or not isinstance(name, str):
        return "Name is required."

    stripped = name.strip()
    if not stripped:
        return "Name is required."

    if len(stripped) > max_length:
        return f"Name must be {max_length} characters or fewer."

    # Check for profanities
    err = sanitize_input(stripped)
    if err:
        return err

    return None


def validate_bio(bio, max_length=500):
    """
    Validate a biography/bio text.

    Checks performed (in order):
      1. Not null (can be empty string after stripping)
      2. At most max_length characters (default 500)
      3. No profanities (via sanitize_input)

    Args:
        bio: The bio text to validate.
        max_length: Maximum allowed length (default: 500).

    Returns:
        None if the bio is acceptable.
        A str error message if the bio is unacceptable.
    """
    if bio is None or not isinstance(bio, str):
        return None  # Bio is optional

    stripped = bio.strip()
    if not stripped:
        return None  # Empty bio is OK (optional field)

    if len(stripped) > max_length:
        return f"Bio must be {max_length} characters or fewer."

    # Check for profanities
    err = sanitize_input(stripped)
    if err:
        return err

    return None
