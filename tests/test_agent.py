"""Tests for the StudyAssistantAgent."""

import pytest

from src.study_agent.agent import StudyAssistantAgent, AgentResponse


class TestStudyAssistantAgent:
    def setup_method(self):
        self.agent = StudyAssistantAgent()

    # ------------------------------------------------------------------
    # Normal workflow
    # ------------------------------------------------------------------

    def test_valid_query_returns_answer(self):
        response = self.agent.run("software testing")
        assert response.is_valid is True
        assert len(response.answer) > 0
        assert response.error is None

    def test_deployment_query_finds_topic(self):
        response = self.agent.run("explain deployment strategies")
        assert response.is_valid is True
        assert "deployment" in response.topics_found

    def test_agent_query_finds_topic(self):
        response = self.agent.run("AI agents and tools")
        assert response.is_valid is True
        assert len(response.topics_found) > 0

    def test_response_contains_next_steps(self):
        response = self.agent.run("software testing best practices")
        assert response.is_valid is True
        assert isinstance(response.next_steps, list)

    def test_python_query(self):
        response = self.agent.run("Python programming language")
        assert response.is_valid is True
        assert len(response.answer) > 0

    # ------------------------------------------------------------------
    # Statistics / calculator path
    # ------------------------------------------------------------------

    def test_statistics_query_uses_calculator(self):
        response = self.agent.run("calculate mean and statistics")
        assert response.is_valid is True
        assert "statistics" in response.topics_found
        assert "Mean" in response.answer or "mean" in response.answer.lower()

    def test_average_keyword_triggers_stats(self):
        response = self.agent.run("what is the average")
        assert response.is_valid is True
        assert "statistics" in response.topics_found

    # ------------------------------------------------------------------
    # Invalid / edge-case input
    # ------------------------------------------------------------------

    def test_empty_input_is_invalid(self):
        response = self.agent.run("")
        assert response.is_valid is False
        assert response.error is not None

    def test_whitespace_only_is_invalid(self):
        response = self.agent.run("   ")
        assert response.is_valid is False

    def test_too_short_is_invalid(self):
        response = self.agent.run("AI")
        assert response.is_valid is False

    # ------------------------------------------------------------------
    # No matching knowledge base result
    # ------------------------------------------------------------------

    def test_unknown_topic_returns_not_found_message(self):
        response = self.agent.run("xylophone manufacturing processes")
        assert response.is_valid is True
        assert response.topics_found == []
        assert "no matching" in response.answer.lower()

    # ------------------------------------------------------------------
    # AgentResponse structure
    # ------------------------------------------------------------------

    def test_response_is_agent_response_type(self):
        response = self.agent.run("testing in Python")
        assert isinstance(response, AgentResponse)

    def test_query_preserved_in_response(self):
        query = "explain deployment"
        response = self.agent.run(query)
        assert response.query == query
