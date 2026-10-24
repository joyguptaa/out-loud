"""CLI entry point for Out Loud."""

from __future__ import annotations

import sys

from .asr.vosk_engine import VoskEngine
from .audio.pipeline import SpeechPipeline
from .models.registry import available_languages
from .sanitizer.cleaner import TextCleaner


# ── Display callbacks ────────────────────────────────────────────────────────

_CLEAR = "\r\033[K"  # carriage-return + erase-to-end-of-line


def _on_partial(raw: str, cleaned: str) -> None:
    """Overwrite the current terminal line with the latest partial result."""
    display = cleaned or raw
    sys.stdout.write(f"{_CLEAR}  ▸ {display}")
    sys.stdout.flush()


def _on_final(raw: str, cleaned: str) -> None:
    """Print the finished segment as Raw / Clean, then a blank line."""
    sys.stdout.write(_CLEAR)  # wipe the partial line
    if raw != cleaned:
        print(f"  Raw:   {raw}")
        print(f"  Clean: {cleaned}")
    else:
        print(f"  {cleaned}")
    print()


# ── Language picker ──────────────────────────────────────────────────────────

def _choose_language() -> str:
    langs = available_languages()
    print("  Available languages:")
    for idx, (code, name) in enumerate(langs, 1):
        print(f"    [{idx}] {code} – {name}")
    print()

    while True:
        choice = input(f"  Select language [1]: ").strip() or "1"
        try:
            index = int(choice) - 1
            if 0 <= index < len(langs):
                return langs[index][0]
        except ValueError:
            # Maybe they typed the code directly, e.g. "en".
            for code, _ in langs:
                if choice.lower() == code:
                    return code
        print("  Invalid choice – try again.")


# ── Main ─────────────────────────────────────────────────────────────────────

BANNER = r"""
  ╔═══════════════════════════════════════╗
  ║   Out Loud – Voice Sanitizer v0.1.0  ║
  ╚═══════════════════════════════════════╝
"""


def main() -> None:
    print(BANNER)

    try:
        language = _choose_language()
    except (KeyboardInterrupt, EOFError):
        print("\n  Bye!")
        sys.exit(0)

    print()

    engine = VoskEngine()
    cleaner = TextCleaner(language=language)
    pipeline = SpeechPipeline(
        engine=engine,
        cleaner=cleaner,
        on_partial=_on_partial,
        on_final=_on_final,
    )

    try:
        pipeline.run(language)
    except KeyboardInterrupt:
        pass

    print("\n  Bye!")


if __name__ == "__main__":
    main()

