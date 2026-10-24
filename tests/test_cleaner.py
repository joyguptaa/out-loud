"""Unit tests for the TextCleaner."""

from voice_sanitizer.sanitizer.cleaner import TextCleaner


class TestRemoveFillers:
    def test_removes_hesitation_sounds(self) -> None:
        c = TextCleaner("en")
        assert c.clean("uh hello um world") == "hello world"

    def test_removes_multiword_fillers(self) -> None:
        c = TextCleaner("en")
        assert c.clean("so you know it works i mean really") == "so it works really"

    def test_preserves_legitimate_words(self) -> None:
        c = TextCleaner("en")
        assert c.clean("i like this") == "i like this"

    def test_case_insensitive(self) -> None:
        c = TextCleaner("en")
        assert c.clean("UH hello UM world") == "hello world"


class TestCollapseRepeatedWords:
    def test_triple_repeat(self) -> None:
        c = TextCleaner("en")
        assert c.collapse_repeated_words("the the the cat") == "the cat"

    def test_double_repeat(self) -> None:
        c = TextCleaner("en")
        assert c.collapse_repeated_words("i i went") == "i went"

    def test_no_repeat(self) -> None:
        c = TextCleaner("en")
        assert c.collapse_repeated_words("hello world") == "hello world"

    def test_contraction_repeat(self) -> None:
        c = TextCleaner("en")
        assert c.collapse_repeated_words("don't don't do that") == "don't do that"


class TestRemoveRepeatedNgrams:
    def test_bigram_repeat(self) -> None:
        c = TextCleaner("en")
        result = c.remove_repeated_ngrams("i went i went to the store")
        assert result == "i went to the store"

    def test_trigram_repeat(self) -> None:
        c = TextCleaner("en")
        result = c.remove_repeated_ngrams("go to the go to the store")
        assert result == "go to the store"

    def test_no_repeat(self) -> None:
        c = TextCleaner("en")
        result = c.remove_repeated_ngrams("the quick brown fox")
        assert result == "the quick brown fox"


class TestCleanEndToEnd:
    def test_combined(self) -> None:
        c = TextCleaner("en")
        raw = "um so i went i went to the the store you know"
        cleaned = c.clean(raw)
        assert "um" not in cleaned
        assert "you know" not in cleaned
        assert "the the" not in cleaned
        assert "i went i went" not in cleaned
        assert "store" in cleaned

    def test_empty(self) -> None:
        c = TextCleaner("en")
        assert c.clean("") == ""

    def test_only_fillers(self) -> None:
        c = TextCleaner("en")
        assert c.clean("uh um er") == ""

