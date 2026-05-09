"""Integration tests — full pipeline from raw user input to formatted output.

These tests exercise multiple components working together and verify
end-to-end behaviour, data flow between tools, and error propagation.
"""

import pytest
from src.study_agent.agent import StudyAssistantAgent, AgentResponse
from src.study_agent.tools.validator import ValidatorTool
from src.study_agent.tools.search_tool import SearchTool
from src.study_agent.tools.file_reader import FileReaderTool
from src.study_agent.tools.calculator import CalculatorTool
from src.study_agent.main import format_response


# ---------------------------------------------------------------------------
# Scenario 1 – Normal knowledge-base lookup (happy path)
# ---------------------------------------------------------------------------

class TestHappyPathWorkflow:
    """Full pipeline for a valid topic that exists in the knowledge base."""

    def setup_method(self):
        self.agent = StudyAssistantAgent()

    def test_testing_topic_returns_structured_answer(self):
        """Query about testing returns a multi-section answer string."""
        resp = self.agent.run("software testing best practices")
        assert resp.is_valid
        assert "software testing" in resp.topics_found
        assert "software testing" in resp.answer.lower() or "testing" in resp.answer.lower()

    def test_deployment_topic_includes_next_steps(self):
        """Deployment query produces at least one recommended next step."""
        resp = self.agent.run("deployment strategies CI CD")
        assert resp.is_valid
        assert len(resp.next_steps) >= 1

    def test_ai_topic_returns_multiple_sections(self):
        """Broad AI query can match more than one knowledge base section."""
        resp = self.agent.run("artificial intelligence agents and tools")
        assert resp.is_valid
        assert len(resp.topics_found) >= 1

    def test_answer_contains_query_echo(self):
        """The answer text includes the user's original (cleaned) query."""
        resp = self.agent.run("python programming language")
        assert resp.is_valid
        assert resp.query.lower() in resp.answer.lower()

    def test_top_k_cap_respected(self):
        """Agent never returns more than TOP_K topics in a single response."""
        resp = self.agent.run("python statistics deployment testing agents")
        assert resp.is_valid
        assert len(resp.topics_found) <= StudyAssistantAgent.TOP_K


# ---------------------------------------------------------------------------
# Scenario 2 – Statistics / Calculator path
# ---------------------------------------------------------------------------

class TestStatsWorkflow:
    """Queries containing stats keywords route to CalculatorTool."""

    def setup_method(self):
        self.agent = StudyAssistantAgent()

    def test_mean_keyword_uses_calculator(self):
        resp = self.agent.run("what is mean and median")
        assert resp.is_valid
        assert "statistics" in resp.topics_found
        assert "Mean" in resp.answer

    def test_std_dev_keyword_triggers_stats(self):
        resp = self.agent.run("standard deviation std analysis")
        assert resp.is_valid
        assert "Std Dev" in resp.answer

    def test_stats_answer_contains_numeric_values(self):
        """Stats answer must show actual numbers from the demo dataset."""
        resp = self.agent.run("calculate statistics")
        assert resp.is_valid
        # Demo dataset contains these values
        assert "72" in resp.answer or "85" in resp.answer

    def test_stats_next_steps_are_study_oriented(self):
        resp = self.agent.run("average statistics")
        assert resp.is_valid
        assert any("statistic" in step.lower() or "variance" in step.lower()
                   for step in resp.next_steps)


# ---------------------------------------------------------------------------
# Scenario 3 – Invalid input handling
# ---------------------------------------------------------------------------

class TestInvalidInputHandling:
    """Agent must reject bad input before any tool is called."""

    def setup_method(self):
        self.agent = StudyAssistantAgent()

    def test_empty_string_rejected(self):
        resp = self.agent.run("")
        assert not resp.is_valid
        assert resp.error is not None
        assert resp.topics_found == []

    def test_spaces_only_rejected(self):
        resp = self.agent.run("    ")
        assert not resp.is_valid

    def test_single_char_rejected(self):
        resp = self.agent.run("a")
        assert not resp.is_valid

    def test_two_char_rejected(self):
        resp = self.agent.run("AI")
        assert not resp.is_valid

    def test_query_over_500_chars_rejected(self):
        resp = self.agent.run("x" * 501)
        assert not resp.is_valid

    def test_invalid_response_answer_is_empty(self):
        """An invalid response must not accidentally carry an answer body."""
        resp = self.agent.run("")
        assert resp.answer == ""


# ---------------------------------------------------------------------------
# Scenario 4 – No knowledge base match
# ---------------------------------------------------------------------------

class TestNoMatchFallback:
    """When no section matches the query the agent returns a helpful message."""

    def setup_method(self):
        self.agent = StudyAssistantAgent()

    def test_gibberish_query_returns_fallback(self):
        resp = self.agent.run("zgkqmplxtvw nonsense gobbledegook")
        assert resp.is_valid
        assert resp.topics_found == []
        assert "no matching" in resp.answer.lower()

    def test_fallback_suggests_known_topics(self):
        resp = self.agent.run("medieval catapult mechanics")
        assert "testing" in resp.answer.lower() or "agents" in resp.answer.lower()


# ---------------------------------------------------------------------------
# Scenario 5 – Data flow between tools
# ---------------------------------------------------------------------------

class TestDataFlowBetweenTools:
    """Verify that data is correctly passed and converted between tools."""

    def test_validator_output_feeds_search_tool(self):
        """Cleaned query from ValidatorTool must reach SearchTool unchanged."""
        validator = ValidatorTool()
        search = SearchTool()

        raw = "  Python programming  "
        validation = validator.validate(raw)
        assert validation.is_valid
        cleaned = validation.cleaned_query  # "Python programming"

        results = search.search(cleaned)
        assert len(results) > 0
        assert any("python" in r.topic for r in results)

    def test_file_reader_sections_feed_search_scorer(self):
        """FileReaderTool sections must be dicts that SearchTool can score."""
        reader = FileReaderTool()
        sections = reader.read_sections()

        assert isinstance(sections, dict)
        for topic, content in sections.items():
            assert isinstance(topic, str)
            assert isinstance(content, str)
            assert len(content) > 0

    def test_search_result_relevance_scores_are_floats(self):
        search = SearchTool()
        results = search.search("software testing")
        for r in results:
            assert isinstance(r.relevance_score, float)
            assert 0.0 < r.relevance_score

    def test_calculator_describe_output_is_stats_result(self):
        from src.study_agent.tools.calculator import StatsResult
        calc = CalculatorTool()
        result = calc.describe([10, 20, 30, 40, 50])
        assert isinstance(result, StatsResult)
        assert result.count == 5
        assert result.mean == pytest.approx(30.0)
        assert result.minimum == 10
        assert result.maximum == 50


# ---------------------------------------------------------------------------
# Scenario 6 – format_response integration
# ---------------------------------------------------------------------------

class TestFormatResponse:
    """format_response must produce readable text from AgentResponse objects."""

    def setup_method(self):
        self.agent = StudyAssistantAgent()

    def test_valid_response_formats_without_error_prefix(self):
        resp = self.agent.run("software testing")
        text = format_response(resp)
        assert "[ERROR]" not in text
        assert len(text) > 0

    def test_invalid_response_formats_with_error_prefix(self):
        resp = self.agent.run("")
        text = format_response(resp)
        assert "[ERROR]" in text

    def test_next_steps_appear_in_formatted_output(self):
        resp = self.agent.run("software testing")
        text = format_response(resp)
        assert "Next Steps" in text or "1." in text

    def test_verbose_mode_adds_topic_line(self):
        resp = self.agent.run("deployment")
        text = format_response(resp, verbose=True)
        assert "Topics matched" in text

    def test_non_verbose_omits_topic_line(self):
        resp = self.agent.run("deployment")
        text = format_response(resp, verbose=False)
        assert "Topics matched" not in text
