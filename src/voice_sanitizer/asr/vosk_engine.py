"""Vosk-based ASR engine (offline, low-latency)."""

from __future__ import annotations

import json

import numpy as np
import vosk

from .base import ASREngine
from ..models.manager import ModelManager

# Silence Vosk's own debug output.
vosk.SetLogLevel(-1)


class VoskEngine(ASREngine):
    """Wraps a ``vosk.KaldiRecognizer`` behind the :class:`ASREngine` API."""

    def __init__(self) -> None:
        self._model: vosk.Model | None = None
        self._recognizer: vosk.KaldiRecognizer | None = None
        self._manager = ModelManager()
        self._sample_rate: int = 16_000
        self._accumulated: str = ""

    # ── ASREngine interface ──────────────────────────────────────────────

    def load(self, language: str) -> None:
        model_path = self._manager.download(language)
        self._model = vosk.Model(str(model_path))
        self._recognizer = vosk.KaldiRecognizer(self._model, self._sample_rate)
        self._recognizer.SetWords(False)

    def transcribe_chunk(self, audio: np.ndarray) -> str:
        """Feed a chunk and return the full text recognised so far.

        Internally accumulates any finalised segments so the caller always
        sees a single growing string until :meth:`finalize` is called.
        """
        if not self.is_ready():
            return ""

        audio_bytes = audio.astype(np.int16).tobytes()

        if self._recognizer.AcceptWaveform(audio_bytes):
            result = json.loads(self._recognizer.Result())
            text = result.get("text", "")
            if text:
                self._accumulated += (" " + text) if self._accumulated else text
            return self._accumulated
        else:
            partial = json.loads(self._recognizer.PartialResult())
            partial_text = partial.get("partial", "")
            if self._accumulated and partial_text:
                return self._accumulated + " " + partial_text
            return self._accumulated or partial_text

    def is_ready(self) -> bool:
        return self._model is not None and self._recognizer is not None

    # ── Extended helpers ─────────────────────────────────────────────────

    def finalize(self) -> str:
        if not self.is_ready():
            return ""
        result = json.loads(self._recognizer.FinalResult())
        text = result.get("text", "")
        if text:
            self._accumulated += (" " + text) if self._accumulated else text
        final = self._accumulated
        self._accumulated = ""
        return final

    def reset(self) -> None:
        self._accumulated = ""
        if self._model is not None:
            self._recognizer = vosk.KaldiRecognizer(
                self._model, self._sample_rate
            )
            self._recognizer.SetWords(False)

