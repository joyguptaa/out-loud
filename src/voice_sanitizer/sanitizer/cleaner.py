"""Rule-based text cleaner: fillers, repeated words, repeated n-grams."""

from __future__ import annotations

import re

from .fillers import get_fillers


class TextCleaner:
    """Cleans raw ASR output by removing verbal disfluencies."""

    def __init__(self, language: str = "en") -> None:
        self.language = language
        self._fillers = get_fillers(language)
        self._filler_re: re.Pattern[str] | None = self._build_filler_pattern()

    # ── Public API ───────────────────────────────────────────────────────

    def clean(self, text: str) -> str:
        """Apply every cleaning rule and return the result."""
        text = self.remove_fillers(text)
        text = self._normalize_whitespace(text)
        text = self.collapse_repeated_words(text)
        text = self.remove_repeated_ngrams(text)
        text = self._normalize_whitespace(text)
        return text

    def remove_fillers(self, text: str) -> str:
        """Strip filler words / phrases."""
        if self._filler_re is None:
            return text
        return self._filler_re.sub("", text)

    @staticmethod
    def collapse_repeated_words(text: str) -> str:
        r"""Collapse runs of the same word: ``"the the the"`` → ``"the"``."""
        return re.sub(r"\b([\w\']+)(?:\s+\1)+\b", r"\1", text, flags=re.IGNORECASE)

    @staticmethod
    def remove_repeated_ngrams(
        text: str,
        min_n: int = 2,
        max_n: int = 4,
    ) -> str:
        """Remove consecutively repeated n-grams (2–4 words by default)."""
        for n in range(max_n, min_n - 1, -1):
            words = text.split()
            if len(words) < 2 * n:
                continue

            result: list[str] = []
            i = 0
            while i < len(words):
                # Check whether the n-gram starting at *i* repeats immediately.
                if i + 2 * n <= len(words):
                    ngram = [w.lower() for w in words[i : i + n]]
                    next_ngram = [w.lower() for w in words[i + n : i + 2 * n]]
                    if ngram == next_ngram:
                        # Keep the first occurrence, skip all duplicates.
                        result.extend(words[i : i + n])
                        i += 2 * n
                        while i + n <= len(words):
                            following = [w.lower() for w in words[i : i + n]]
                            if following == ngram:
                                i += n
                            else:
                                break
                        continue

                result.append(words[i])
                i += 1

            text = " ".join(result)
        return text

    # ── Internals ────────────────────────────────────────────────────────

    def _build_filler_pattern(self) -> re.Pattern[str] | None:
        if not self._fillers:
            return None
        # Longest match first so multi-word fillers are tried before their
        # single-word sub-parts.
        sorted_fillers = sorted(self._fillers, key=len, reverse=True)
        escaped = [re.escape(f) for f in sorted_fillers]
        return re.compile(r"\b(?:" + "|".join(escaped) + r")\b", re.IGNORECASE)

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

