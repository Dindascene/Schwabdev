"""
Schwabdev URL Constants and Validation.
Defines allowed API base URLs for production and testing environments.
"""

import re

SCHWAB_API_URL = "https://api.schwabapi.com"

# Default SimSchwab URL (convenience constant, any localhost port is valid)
SIMSCHWAB_API_URL = "http://localhost:9004"

# Pattern for SimSchwab localhost URLs (any port)
_SIMSCHWAB_PATTERN = re.compile(r"^http://localhost:\d+$")


def is_valid_base_url(url: str) -> bool:
    """
    Validate base_url is either production Schwab or localhost SimSchwab.

    Args:
        url: The base URL to validate

    Returns:
        True if URL is valid (production Schwab or localhost), False otherwise
    """
    if url == SCHWAB_API_URL:
        return True
    if _SIMSCHWAB_PATTERN.match(url):
        return True
    return False


def is_simschwab_url(url: str) -> bool:
    """
    Check if URL is a SimSchwab localhost URL.

    Args:
        url: The URL to check

    Returns:
        True if URL matches localhost pattern, False otherwise
    """
    return bool(_SIMSCHWAB_PATTERN.match(url))
