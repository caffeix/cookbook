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
from markupsafe import Markup

# Temporary work-around for tool icons
ICON_SVGS = {
    "microwave": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="14" rx="2"/><rect x="5" y="7" width="9" height="8" rx="1"/><path d="M7 10c.8-.8 1.7-.8 2.5 0s1.7.8 2.5 0"/><line x1="17" y1="8" x2="19" y2="8"/><line x1="17" y1="11" x2="19" y2="11"/><circle cx="18" cy="14.5" r="0.75" fill="currentColor"/><line x1="6" y1="18" x2="6" y2="20"/><line x1="18" y1="18" x2="18" y2="20"/></svg>',
    "air-fryer": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="14" height="18" rx="4"/><rect x="7" y="11" width="10" height="8" rx="2"/><line x1="10" y1="6" x2="14" y2="6"/><line x1="12" y1="13" x2="12" y2="15"/></svg>',
    "frying-pan": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11h11a1 1 0 0 1 1 1v1a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5v-1a1 1 0 0 1 1-1z"/><path d="M15 13h6a1 1 0 0 0 1-1v0a1 1 0 0 0-1-1h-6"/></svg>',
    "stovetop": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="14" rx="2"/><circle cx="8" cy="11" r="2"/><circle cx="16" cy="11" r="2"/><line x1="2" y1="6" x2="22" y2="6"/></svg>',
    "oven": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><rect x="6" y="8" width="12" height="7"/><circle cx="8" cy="17" r="1"/><circle cx="12" cy="17" r="1"/><circle cx="16" cy="17" r="1"/></svg>',
    "blender": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6v4H9z"/><path d="M8 7l1 10h6l1-10z"/><rect x="7" y="17" width="10" height="4" rx="1"/></svg>',
    "whisk": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15v6"/><path d="M12 3c-3 0-5 3-5 6.5C7 12.5 12 15 12 15s5-2.5 5-5.5C17 6 15 3 12 3z"/><path d="M12 3c-1.5 0-2.5 3-2.5 6.5C9.5 12 12 15 12 15s2.5-3 2.5-5.5C14.5 6 13.5 3 12 3z"/></svg>',
    "potato-masher": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6"/><line x1="12" y1="3" x2="12" y2="13"/><path d="M6 14h12"/><line x1="6" y1="14" x2="6" y2="17"/><line x1="18" y1="14" x2="18" y2="17"/><path d="M6 17c.6-1.2 1.4-1.2 2 0s1.4 1.2 2 0 1.4-1.2 2 0 1.4 1.2 2 0 1.4-1.2 2 0"/></svg>',
    "ladle": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 3a2 2 0 0 0-2 2v9"/><path d="M6 14c0 3.5 3 6 7 6s7-2.5 7-6H6z"/></svg>',
    "large-pot": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 9h14v8a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3V9z"/><path d="M4 9h16"/><path d="M9 6.5h6"/><path d="M2 12h3"/><path d="M19 12h3"/></svg>',
    "small-pot": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M7 10h10v6a3 3 0 0 1-3 3h-4a3 3 0 0 1-3-3v-6z"/><path d="M5 10h14"/><path d="M10 7.5h4"/><path d="M3 12h2"/><path d="M19 12h2"/></svg>',
    "spatula": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 12v9"/><rect x="8" y="3" width="8" height="9" rx="1"/><line x1="10" y1="5" x2="10" y2="9"/><line x1="14" y1="5" x2="14" y2="9"/></svg>',
    "scale": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><path d="M6 7.5l6-3 6 3"/><path d="M4 14l4-6.5"/><path d="M20 14l-4-6.5"/><rect x="2" y="14" width="8" height="2" rx="1"/><rect x="14" y="14" width="8" height="2" rx="1"/></svg>',
    "peeler": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21v-9"/><path d="M8 5h8v4a4 4 0 0 1-8 0V5z"/><line x1="9" y1="7" x2="15" y2="7"/></svg>',
}


def render_icon(val: str | None) -> Markup:
    """Render an icon key, raw SVG, or emoji as safe HTML markup."""
    if not val:
        return Markup("")
    if val in ICON_SVGS:
        return Markup(ICON_SVGS[val])
    return Markup(val)


def remove_filter(query_string: bytes | str, param: str, val: str | int) -> str:
    """Helper to remove a specific value from a comma-separated query parameter in Jinja templates."""
    from urllib.parse import parse_qs, urlencode
    qs = query_string.decode("utf-8") if isinstance(query_string, bytes) else (query_string or "")
    parsed = parse_qs(qs)
    val_str = str(val)
    if param in parsed:
        items = []
        for item in parsed[param]:
            for sub in item.split(","):
                sub_str = sub.strip()
                if sub_str and sub_str != val_str:
                    items.append(sub_str)
        if items:
            parsed[param] = [",".join(items)]
        else:
            del parsed[param]
    return urlencode(parsed, doseq=True)


