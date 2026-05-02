"""Core Study Assistant Agent — orchestrates tools to answer study queries."""

from dataclasses import dataclass, field
from typing import Optional

from .tools.validator import ValidatorTool
from .tools.search_tool import SearchTool, SearchResult
from .tools.file_reader import FileReaderTool
from .tools.calculator import CalculatorTool


@dataclass
class AgentResponse:
    query: str
    is_valid: bool
    topics_found: list[str]
    answer: str
    next_steps: list[str] = field(default_factory=list)
    error: Optional[str] = None


# Hints for numeric / statistics questions
_STATS_TRIGGERS = {"mean", "average", "median", "statistics", "calculate", "percent", "std"}


class StudyAssistantAgent:
    """An agent that classifies study queries and answers them using local tools.

    Workflow:
        1. Validate input.
        2. Classify whether the query needs a stats calculation.
        3. Search the knowledge base for relevant sections.
        4. Synthesise a structured answer.
    """

    TOP_K = 3  # max sections to include in the answer

    def __init__(
        self,
        validator: Optional[ValidatorTool] = None,
        search_tool: Optional[SearchTool] = None,
        calculator: Optional[CalculatorTool] = None,
    ) -> None:
        self.validator = validator or ValidatorTool()
        self.search_tool = search_tool or SearchTool()
        self.calculator = calculator or CalculatorTool()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, raw_query: str) -> AgentResponse:
        """Process a raw user query and return a structured AgentResponse."""

        # Step 1 – validate
        validation = self.validator.validate(raw_query)
        if not validation.is_valid:
            return AgentResponse(
                query=raw_query,
                is_valid=False,
                topics_found=[],
                answer="",
                error=validation.message,
            )

        query = validation.cleaned_query

        # Step 2 – classify: does the user want a stats demo?
        if self._wants_stats(query):
            return self._handle_stats_query(query)

        # Step 3 – search knowledge base
        results = self.search_tool.search(query)

        if not results:
            return AgentResponse(
                query=query,
                is_valid=True,
                topics_found=[],
                answer=(
                    "No matching topics were found in the knowledge base for your query.\n"
                    "Try rephrasing or use one of these topics: "
                    "testing, deployment, AI, agents, Python, statistics."
                ),
                next_steps=["Broaden your search terms.", "Add new notes to the knowledge base."],
            )

        # Step 4 – synthesise answer
        top = results[: self.TOP_K]
        topics_found = [r.topic for r in top]
        answer = self._build_answer(query, top)
        next_steps = self._suggest_next_steps(topics_found)

        return AgentResponse(
            query=query,
            is_valid=True,
            topics_found=topics_found,
            answer=answer,
            next_steps=next_steps,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _wants_stats(self, query: str) -> bool:
        words = {w.lower() for w in query.split()}
        return bool(words & _STATS_TRIGGERS)

    def _handle_stats_query(self, query: str) -> AgentResponse:
        """Return a statistics demo answer using the CalculatorTool."""
        demo_values = [72, 85, 91, 68, 79, 88, 95, 74]
        stats = self.calculator.describe(demo_values)
        answer = (
            f"Statistics Demo (sample dataset: {demo_values})\n"
            f"  Count      : {stats.count}\n"
            f"  Mean       : {stats.mean}\n"
            f"  Median     : {stats.median}\n"
            f"  Std Dev    : {stats.std_dev}\n"
            f"  Min / Max  : {stats.minimum} / {stats.maximum}\n\n"
            "These are the core descriptive statistics used in data analysis and AI model evaluation."
        )
        return AgentResponse(
            query=query,
            is_valid=True,
            topics_found=["statistics"],
            answer=answer,
            next_steps=[
                "Study variance and standard deviation formulas.",
                "Look into how statistics relate to AI model evaluation metrics.",
            ],
        )

    def _build_answer(self, query: str, results: list[SearchResult]) -> str:
        lines: list[str] = [
            f'Study Answer for: "{query}"',
            "=" * 60,
        ]
        for result in results:
            lines.append(f"\n### Topic: {result.topic.title()}")
            lines.append(f"(Relevance: {result.relevance_score:.0%})\n")
            # Trim very long sections to keep output readable
            body = result.content
            if len(body) > 800:
                body = body[:800].rsplit("\n", 1)[0] + "\n... [truncated]"
            lines.append(body)

        return "\n".join(lines)

    def _suggest_next_steps(self, topics: list[str]) -> list[str]:
        suggestions_map: dict[str, list[str]] = {
            "software testing": [
                "Write a small pytest suite for a sample project.",
                "Learn about Test-Driven Development (TDD).",
            ],
            "deployment": [
                "Set up a simple GitHub Actions CI/CD pipeline.",
                "Study Docker basics for containerised deployment.",
            ],
            "artificial intelligence": [
                "Explore a beginner ML tutorial with scikit-learn.",
                "Read about supervised vs unsupervised learning.",
            ],
            "agents": [
                "Implement a second agent tool (e.g. a web search stub).",
                "Study ReAct and Chain-of-Thought prompting patterns.",
            ],
            "python programming": [
                "Practice with Python type hints and dataclasses.",
                "Read PEP 8 — the Python style guide.",
            ],
            "statistics": [
                "Review mean, median, and standard deviation calculations.",
                "Connect statistics concepts to AI evaluation metrics.",
            ],
        }
        steps: list[str] = []
        for topic in topics:
            steps.extend(suggestions_map.get(topic, []))
        return steps[:4]  # cap at 4 suggestions
