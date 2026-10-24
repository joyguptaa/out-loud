"""Unit tests for model registry and manager."""

from pathlib import Path
import pytest

from voice_sanitizer.models.registry import available_languages, get_model_info
from voice_sanitizer.models.manager import ModelManager


def test_registry_has_supported_languages() -> None:
    langs = available_languages()
    lang_codes = [code for code, _ in langs]
    assert "en" in lang_codes
    assert "es" in lang_codes


def test_registry_get_model_info() -> None:
    en_info = get_model_info("en")
    assert en_info is not None
    assert "name" in en_info
    assert "url" in en_info

    invalid = get_model_info("nonexistent_lang")
    assert invalid is None


def test_model_manager_path_resolution(tmp_path: Path) -> None:
    manager = ModelManager(models_dir=tmp_path)
    path = manager.get_model_path("en")
    assert isinstance(path, Path)
    assert "vosk-model" in path.name
    assert path.parent == tmp_path

    with pytest.raises(ValueError):
        manager.get_model_path("nonexistent_lang")
