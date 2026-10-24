"""Read-only catalogue browsing helpers."""
from urllib.parse import urlsplit


def safe_url(value):
    try:
        u = urlsplit(value)
        return value if u.scheme == "https" and u.hostname and not u.username else None
    except (ValueError, TypeError):
        return None


def study_units(catalog, track):
    """Show every session for a track without requiring device progress."""
    skills = {skill["id"]: skill for skill in catalog["skills"]}
    return [unit for unit in catalog["units"]
            if "core" in skills[unit["skill"]]["tracks"]
            or track in skills[unit["skill"]]["tracks"]]
