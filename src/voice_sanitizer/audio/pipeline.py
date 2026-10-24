"""Real-time speech pipeline: Mic → Silero VAD → ASR → TextCleaner."""

from __future__ import annotations

import sys
from collections.abc import Callable

import numpy as np

from ..asr.base import ASREngine
from ..sanitizer.cleaner import TextCleaner
from ..utils.config import (
    MIN_SILENCE_DURATION_MS,
    SAMPLE_RATE,
    SPEECH_PAD_MS,
    VAD_THRESHOLD,
)
from .recorder import MicRecorder

# Type alias for the callbacks the CLI passes in.
TextCallback = Callable[[str, str], None]  # (raw, cleaned)


class SpeechPipeline:
    """Orchestrates the full Mic → VAD → ASR → Cleaner loop.

    Parameters
    ----------
    engine:
        An :class:`ASREngine` instance (e.g. :class:`VoskEngine`).
    cleaner:
        A :class:`TextCleaner` configured for the target language.
    on_partial:
        Called with ``(raw_text, cleaned_text)`` on every partial update.
    on_final:
        Called with ``(raw_text, cleaned_text)`` when a speech segment ends.
    """

    def __init__(
        self,
        engine: ASREngine,
        cleaner: TextCleaner,
        on_partial: TextCallback | None = None,
        on_final: TextCallback | None = None,
    ) -> None:
        self._engine = engine
        self._cleaner = cleaner
        self._on_partial = on_partial
        self._on_final = on_final
        self._recorder = MicRecorder()
        self._running = False

    # ── Public API ───────────────────────────────────────────────────────

    def run(self, language: str) -> None:
        """Block and process audio until interrupted (Ctrl-C)."""
        # Late-import so the heavy ONNX model is only loaded when needed.
        from silero_vad import VADIterator, load_silero_vad  # type: ignore[import-untyped]

        print("  Loading VAD model …")
        vad_model = load_silero_vad()
        vad_iterator = VADIterator(
            vad_model,
            threshold=VAD_THRESHOLD,
            sampling_rate=SAMPLE_RATE,
            min_silence_duration_ms=MIN_SILENCE_DURATION_MS,
            speech_pad_ms=SPEECH_PAD_MS,
        )
        print("  ✓ VAD ready")

        print(f"  Loading ASR model ({language}) …")
        self._engine.load(language)
        print("  ✓ ASR ready\n")

        print("  Listening … press Ctrl+C to stop.\n")

        self._running = True
        is_speaking = False

        with self._recorder:
            try:
                while self._running:
                    chunk = self._recorder.read()
                    if chunk is None:
                        continue

                    # Silero VAD expects float32 in [-1, 1].
                    chunk_f32 = chunk.astype(np.float32) / 32768.0
                    vad_event = vad_iterator(chunk_f32)

                    # ── Speech start ─────────────────────────────────
                    if vad_event and "start" in vad_event:
                        is_speaking = True
                        self._engine.reset()

                    # ── During speech → feed ASR ─────────────────────
                    if is_speaking:
                        text = self._engine.transcribe_chunk(chunk)
                        if text and self._on_partial:
                            self._on_partial(text, self._cleaner.clean(text))

                    # ── Speech end ───────────────────────────────────
                    if vad_event and "end" in vad_event:
                        is_speaking = False
                        final_text = self._engine.finalize()
                        if final_text and self._on_final:
                            self._on_final(
                                final_text, self._cleaner.clean(final_text)
                            )

            except KeyboardInterrupt:
                # Flush anything still buffered in the recogniser.
                if is_speaking:
                    final_text = self._engine.finalize()
                    if final_text and self._on_final:
                        self._on_final(
                            final_text, self._cleaner.clean(final_text)
                        )
            finally:
                self._running = False
                vad_iterator.reset_states()

    def stop(self) -> None:
        """Signal the processing loop to exit."""
        self._running = False
