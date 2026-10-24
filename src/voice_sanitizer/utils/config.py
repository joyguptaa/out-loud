"""Application-wide configuration constants."""

from pathlib import Path

# ── Directories ──────────────────────────────────────────────────────────────
CONFIG_DIR = Path.home() / "Library" / "Application Support" / "VoiceSanitizer"
MODELS_DIR = CONFIG_DIR / "models"
CACHE_DIR = CONFIG_DIR


# ── Audio ────────────────────────────────────────────────────────────────────
SAMPLE_RATE = 16_000       # Hz – required by both Silero VAD and Vosk
CHANNELS = 1               # Mono
BLOCK_SIZE = 512            # Samples per block (32 ms at 16 kHz)
DTYPE = "int16"

# ── VAD ──────────────────────────────────────────────────────────────────────
VAD_THRESHOLD = 0.5
MIN_SILENCE_DURATION_MS = 500   # Silence needed to end a speech segment
SPEECH_PAD_MS = 30              # Padding around speech boundaries


def ensure_dirs() -> None:
    """Create config and models directories if they don't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

