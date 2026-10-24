"""Language-specific filler / hesitation word lists."""

from __future__ import annotations

# Words that are *almost always* fillers when they appear in ASR output.
# Intentionally conservative – ambiguous words like "so", "like", "well",
# "right" are omitted because they are too often legitimate.
FILLERS: dict[str, list[str]] = {
    "en": [
        # Pure hesitation sounds
        "uh",
        "um",
        "uhm",
        "umm",
        "uh huh",
        "mm",
        "mmm",
        "hmm",
        "hm",
        "ah",
        "er",
        "erm",
        "eh",
        # Discourse markers (very high filler-probability in speech)
        "you know",
        "i mean",
        "sort of",
        "kind of",
        "you know what i mean",
    ],
}


def get_fillers(language: str) -> list[str]:
    """Return the filler list for *language*, or an empty list."""
    return FILLERS.get(language, [])

