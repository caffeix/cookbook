"""Shared utility functions for the cookbook app."""
import re
import unicodedata


def slugify(text: str) -> str:
    """Convert a string to a URL-safe slug.

    Examples:
        "Italian"    -> "italian"
        "Olive Oil"  -> "olive-oil"
        "Quick & Easy" -> "quick-easy"
    """
    # Normalize unicode (é -> e, ñ -> n, etc.)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    # Lowercase
    text = text.lower()
    # Replace any non-alphanumeric character (spaces, punctuation) with a hyphen
    text = re.sub(r"[^a-z0-9]+", "-", text)
    # Strip leading/trailing hyphens and collapse multiples
    text = text.strip("-")
    return text
