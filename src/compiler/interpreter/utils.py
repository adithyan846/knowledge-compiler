"""Shared text cleaning utilities for interpreters."""

def clean_text(text: str) -> str:
    """
    Normalise text: remove Markdown headers, collapse whitespace,
    strip leading/trailing spaces, and remove trailing period.
    """
    if not text:
        return ""
    # Remove leading '#' and any following whitespace (Markdown heading)
    if text.startswith("#"):
        text = text.lstrip("#").lstrip()
    # Collapse whitespace
    text = " ".join(text.split())
    # Remove trailing period (common in sentences)
    if text.endswith("."):
        text = text[:-1].strip()
    return text
