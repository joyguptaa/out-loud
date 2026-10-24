"""Download and cache ASR models."""

from __future__ import annotations

import sys
import urllib.request
import zipfile
from pathlib import Path

from ..utils.config import MODELS_DIR, ensure_dirs
from .registry import get_model_info


class ModelManager:
    """Handles downloading, extracting, and locating ASR model files."""

    def __init__(self, models_dir: Path | None = None) -> None:
        self.models_dir = models_dir or MODELS_DIR
        try:
            self.models_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass

    def get_model_path(self, language: str) -> Path:
        """Return the expected local path for the model (may not exist yet)."""
        info = get_model_info(language)
        if info is None:
            raise ValueError(f"No model registered for language '{language}'")
        return self.models_dir / info["name"]

    def is_downloaded(self, language: str) -> bool:
        """Check whether the model is already cached locally."""
        path = self.get_model_path(language)
        return path.is_dir() and any(path.iterdir())

    def download(self, language: str) -> Path:
        """Download and extract the model if it isn't cached yet.

        Returns the path to the extracted model directory.
        """
        if self.is_downloaded(language):
            return self.get_model_path(language)

        info = get_model_info(language)
        if info is None:
            raise ValueError(f"No model registered for language '{language}'")

        model_path = self.models_dir / info["name"]
        zip_path = self.models_dir / f"{info['name']}.zip"

        print(f"  Downloading {info['name']} …")
        self._download_with_progress(info["url"], zip_path)

        print("  Extracting …")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(self.models_dir)

        zip_path.unlink(missing_ok=True)
        print(f"  ✓ Model ready at {model_path}")
        return model_path

    # ── Internals ────────────────────────────────────────────────────────

    @staticmethod
    def _download_with_progress(url: str, dest: Path) -> None:
        def _report(block_num: int, block_size: int, total_size: int) -> None:
            downloaded = block_num * block_size
            if total_size > 0:
                pct = min(100, downloaded * 100 // total_size)
                mb_dl = downloaded / (1024 * 1024)
                mb_tot = total_size / (1024 * 1024)
                sys.stdout.write(f"\r    {pct:3d}%  ({mb_dl:.1f} / {mb_tot:.1f} MB)")
                sys.stdout.flush()

        urllib.request.urlretrieve(url, str(dest), _report)
        sys.stdout.write("\n")

