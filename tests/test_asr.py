"""Unit tests for the ASR engine interface."""

import numpy as np
import pytest

from voice_sanitizer.asr.base import ASREngine


class DummyEngine(ASREngine):
    def __init__(self) -> None:
        self.loaded_lang = ""

    def load(self, language: str) -> None:
        self.loaded_lang = language

    def transcribe_chunk(self, audio: np.ndarray) -> str:
        return f"transcribed_{len(audio)}"

    def is_ready(self) -> bool:
        return bool(self.loaded_lang)


def test_cannot_instantiate_abstract_asr_engine() -> None:
    with pytest.raises(TypeError):
        ASREngine()  # type: ignore[abstract]


def test_dummy_engine_implements_interface() -> None:
    engine = DummyEngine()
    assert not engine.is_ready()
    engine.load("en")
    assert engine.is_ready()
    assert engine.transcribe_chunk(np.zeros(512, dtype=np.int16)) == "transcribed_512"
    assert engine.finalize() == ""
    engine.reset()
