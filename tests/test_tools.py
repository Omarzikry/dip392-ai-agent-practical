"""Tests for individual tool modules."""

import pytest
from pathlib import Path

from src.study_agent.tools.validator import ValidatorTool
from src.study_agent.tools.file_reader import FileReaderTool
from src.study_agent.tools.search_tool import SearchTool
from src.study_agent.tools.calculator import CalculatorTool


# ---------------------------------------------------------------------------
# ValidatorTool
# ---------------------------------------------------------------------------

class TestValidatorTool:
    def setup_method(self):
        self.v = ValidatorTool()

    def test_valid_query(self):
        result = self.v.validate("software testing")
        assert result.is_valid is True
        assert result.cleaned_query == "software testing"

    def test_empty_string_is_invalid(self):
        result = self.v.validate("")
        assert result.is_valid is False
        assert "empty" in result.message.lower()

    def test_whitespace_only_is_invalid(self):
        result = self.v.validate("   ")
        assert result.is_valid is False

    def test_too_short_is_invalid(self):
        result = self.v.validate("ai")
        assert result.is_valid is False
        assert "short" in result.message.lower()

    def test_too_long_is_truncated(self):
        long_query = "x" * 600
        result = self.v.validate(long_query)
        assert result.is_valid is False
        assert len(result.cleaned_query) <= 500

    def test_strips_leading_trailing_whitespace(self):
        result = self.v.validate("  testing  ")
        assert result.cleaned_query == "testing"


# ---------------------------------------------------------------------------
# FileReaderTool
# ---------------------------------------------------------------------------

class TestFileReaderTool:
    def setup_method(self):
        self.reader = FileReaderTool()

    def test_read_returns_non_empty_string(self):
        content = self.reader.read()
        assert isinstance(content, str)
        assert len(content) > 0

    def test_read_sections_returns_dict(self):
        sections = self.reader.read_sections()
        assert isinstance(sections, dict)
        assert len(sections) > 0

    def test_known_section_present(self):
        sections = self.reader.read_sections()
        assert "software testing" in sections

    def test_missing_file_raises(self, tmp_path):
        reader = FileReaderTool(knowledge_base_path=tmp_path / "nonexistent.md")
        with pytest.raises(FileNotFoundError):
            reader.read()


# ---------------------------------------------------------------------------
# SearchTool
# ---------------------------------------------------------------------------

class TestSearchTool:
    def setup_method(self):
        self.search = SearchTool()

    def test_known_topic_returns_results(self):
        results = self.search.search("software testing")
        assert len(results) > 0
        topics = [r.topic for r in results]
        assert "software testing" in topics

    def test_results_sorted_by_relevance(self):
        results = self.search.search("testing deployment")
        scores = [r.relevance_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_unknown_topic_returns_empty(self):
        results = self.search.search("xyznonexistentterm123")
        assert results == []

    def test_short_query_with_stop_words_returns_empty(self):
        # purely stop words — after filtering nothing remains
        results = self.search.search("what is the")
        assert results == []

    def test_result_has_content(self):
        results = self.search.search("Python programming")
        assert len(results) > 0
        assert all(r.content for r in results)

    def test_relevance_score_between_zero_and_positive(self):
        results = self.search.search("agents tools")
        for r in results:
            assert r.relevance_score > 0


# ---------------------------------------------------------------------------
# CalculatorTool
# ---------------------------------------------------------------------------

class TestCalculatorTool:
    def setup_method(self):
        self.calc = CalculatorTool()

    def test_add(self):
        assert self.calc.add(3, 4) == 7

    def test_subtract(self):
        assert self.calc.subtract(10, 3) == 7

    def test_multiply(self):
        assert self.calc.multiply(3, 4) == 12

    def test_divide(self):
        assert self.calc.divide(10, 2) == 5.0

    def test_divide_by_zero_raises(self):
        with pytest.raises(ValueError, match="zero"):
            self.calc.divide(5, 0)

    def test_percentage(self):
        assert self.calc.percentage(25, 100) == 25.0

    def test_percentage_zero_total_raises(self):
        with pytest.raises(ValueError):
            self.calc.percentage(5, 0)

    def test_describe_basic(self):
        stats = self.calc.describe([2, 4, 6, 8])
        assert stats.count == 4
        assert stats.mean == 5.0
        assert stats.minimum == 2
        assert stats.maximum == 8

    def test_describe_single_value(self):
        stats = self.calc.describe([42])
        assert stats.count == 1
        assert stats.mean == 42
        assert stats.std_dev == 0.0

    def test_describe_empty_raises(self):
        with pytest.raises(ValueError):
            self.calc.describe([])
