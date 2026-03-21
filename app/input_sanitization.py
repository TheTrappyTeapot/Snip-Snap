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
