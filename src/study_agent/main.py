"""CLI entry point for the AI Study Assistant Agent.

Usage:
    python -m study_agent.main "testing and deployment"
    python -m study_agent.main --verbose "explain AI agents"
"""

import argparse
import sys
from typing import Optional

from .agent import StudyAssistantAgent, AgentResponse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="study_agent",
        description="AI Study Assistant — answers study questions using a local knowledge base.",
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="",
        help="Your study topic or question (wrap in quotes if it contains spaces).",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show additional details such as relevance scores.",
    )
    return parser


def format_response(response: AgentResponse, verbose: bool = False) -> str:
    lines: list[str] = []

    if not response.is_valid:
        lines.append(f"[ERROR] {response.error}")
        return "\n".join(lines)

    lines.append(response.answer)

    if response.next_steps:
        lines.append("\n--- Recommended Next Steps ---")
        for i, step in enumerate(response.next_steps, 1):
            lines.append(f"  {i}. {step}")

    if verbose and response.topics_found:
        lines.append(f"\n[Topics matched: {', '.join(response.topics_found)}]")

    return "\n".join(lines)


def main(argv: Optional[list] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.query.strip():
        parser.print_help()
        print("\n[ERROR] Please provide a query. Example:\n  python -m study_agent.main \"software testing\"")
        return 1

    agent = StudyAssistantAgent()
    response = agent.run(args.query)
    print(format_response(response, verbose=args.verbose))

    return 0 if response.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
