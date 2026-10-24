"""Abstract base class that every ASR engine must implement."""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class ASREngine(ABC):
    """Uniform interface for speech-recognition back-ends."""

    @abstractmethod
    def load(self, language: str) -> None:
        """Download (if needed) and load the model for *language* (ISO 639-1)."""

    @abstractmethod
    def transcribe_chunk(self, audio: np.ndarray) -> str:
        """Feed an audio chunk and return the best current transcription.

        For streaming engines this may return a *partial* result that grows
        as more audio arrives, or a *final* result when the engine decides
        a sentence boundary has been reached.
        """

    @abstractmethod
    def is_ready(self) -> bool:
        """Return ``True`` when the engine is loaded and can accept audio."""

    # ── Optional overrides ───────────────────────────────────────────────

    def finalize(self) -> str:
        """Force-finalize any buffered audio and return remaining text.

        Called by the pipeline when VAD detects the end of a speech segment.
        """
        return ""

    def reset(self) -> None:
        """Reset internal state so the next chunk starts a fresh utterance."""

