"""Registry of available ASR models and their download URLs."""

from __future__ import annotations

# Vosk "small" models – fast enough for real-time, light on disk.
VOSK_MODELS: dict[str, dict[str, str]] = {
    "en": {
        "name": "vosk-model-small-en-us-0.15",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
        "lang_name": "English",
    },
    "es": {
        "name": "vosk-model-small-es-0.42",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip",
        "lang_name": "Spanish",
    },
    "fr": {
        "name": "vosk-model-small-fr-0.22",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip",
        "lang_name": "French",
    },
    "de": {
        "name": "vosk-model-small-de-0.15",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip",
        "lang_name": "German",
    },
    "it": {
        "name": "vosk-model-small-it-0.22",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-it-0.22.zip",
        "lang_name": "Italian",
    },
    "pt": {
        "name": "vosk-model-small-pt-0.3",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip",
        "lang_name": "Portuguese",
    },
}


def get_model_info(language: str) -> dict[str, str] | None:
    """Return model metadata for *language*, or ``None``."""
    return VOSK_MODELS.get(language)


def available_languages() -> list[tuple[str, str]]:
    """Return ``[(code, name), ...]`` for every registered language."""
    return [(code, info["lang_name"]) for code, info in VOSK_MODELS.items()]

