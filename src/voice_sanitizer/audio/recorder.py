"""Microphone capture using *sounddevice*."""

from __future__ import annotations

import queue

import numpy as np
import sounddevice as sd

from ..utils.config import BLOCK_SIZE, CHANNELS, DTYPE, SAMPLE_RATE


class MicRecorder:
    """Streams audio from the default input device.

    Usage::

        with MicRecorder() as mic:
            while True:
                chunk = mic.read()
                if chunk is not None:
                    process(chunk)
    """

    def __init__(
        self,
        sample_rate: int = SAMPLE_RATE,
        block_size: int = BLOCK_SIZE,
    ) -> None:
        self.sample_rate = sample_rate
        self.block_size = block_size
        self._queue: queue.Queue[np.ndarray] = queue.Queue()
        self._stream: sd.InputStream | None = None

    # ── Lifecycle ────────────────────────────────────────────────────────

    def start(self) -> None:
        """Open the audio stream."""
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=CHANNELS,
            dtype=DTYPE,
            blocksize=self.block_size,
            callback=self._callback,
        )
        self._stream.start()

    def stop(self) -> None:
        """Close the audio stream."""
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    # ── Reading ──────────────────────────────────────────────────────────

    def read(self, timeout: float = 0.1) -> np.ndarray | None:
        """Return the next audio block, or ``None`` on timeout."""
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

    # ── Context manager ──────────────────────────────────────────────────

    def __enter__(self) -> MicRecorder:
        self.start()
        return self

    def __exit__(self, *_exc: object) -> None:
        self.stop()

    # ── Internals ────────────────────────────────────────────────────────

    def _callback(
        self,
        indata: np.ndarray,
        _frames: int,
        _time: object,
        _status: sd.CallbackFlags,
    ) -> None:
        # indata shape: (block_size, channels) – squeeze to 1-D.
        self._queue.put(indata[:, 0].copy())

