"""Tests for the CLI entry point (main.py).

These tests call main() with a controlled argv list and verify the
exit code and printed output without launching a subprocess.
"""

import pytest
from io import StringIO
from unittest.mock import patch

from src.study_agent.main import main, build_parser, format_response
from src.study_agent.agent import AgentResponse


# ---------------------------------------------------------------------------
# build_parser
# ---------------------------------------------------------------------------

class TestBuildParser:
    def test_parser_accepts_query_positional(self):
        parser = build_parser()
        args = parser.parse_args(["software testing"])
        assert args.query == "software testing"

    def test_parser_verbose_flag_default_false(self):
        parser = build_parser()
        args = parser.parse_args(["something"])
        assert args.verbose is False

    def test_parser_verbose_flag_short(self):
        parser = build_parser()
        args = parser.parse_args(["-v", "query"])
        assert args.verbose is True

    def test_parser_verbose_flag_long(self):
        parser = build_parser()
        args = parser.parse_args(["--verbose", "query"])
        assert args.verbose is True

    def test_parser_no_query_defaults_to_empty_string(self):
        parser = build_parser()
        args = parser.parse_args([])
        assert args.query == ""


# ---------------------------------------------------------------------------
# main() exit codes
# ---------------------------------------------------------------------------

class TestMainExitCodes:
    def test_valid_query_exits_zero(self, capsys):
        code = main(["software testing"])
        assert code == 0

    def test_empty_query_exits_one(self, capsys):
        code = main([])
        assert code == 1

    def test_whitespace_query_exits_one(self, capsys):
        code = main(["   "])
        assert code == 1

    def test_invalid_too_short_exits_one(self, capsys):
        # "AI" is only 2 chars — fails ValidatorTool
        code = main(["AI"])
        assert code == 1

    def test_unknown_topic_still_exits_zero(self, capsys):
        # No match is a valid (handled) case, not an error
        code = main(["zqxwvbnmplkojih"])
        assert code == 0


# ---------------------------------------------------------------------------
# main() output content
# ---------------------------------------------------------------------------

class TestMainOutput:
    def test_valid_query_prints_answer(self, capsys):
        main(["software testing"])
        out = capsys.readouterr().out
        assert len(out.strip()) > 0
        assert "[ERROR]" not in out

    def test_invalid_query_prints_error_line(self, capsys):
        main(["AI"])
        out = capsys.readouterr().out
        assert "[ERROR]" in out

    def test_verbose_flag_adds_topics_line(self, capsys):
        main(["--verbose", "python programming"])
        out = capsys.readouterr().out
        assert "Topics matched" in out

    def test_no_verbose_omits_topics_line(self, capsys):
        main(["python programming"])
        out = capsys.readouterr().out
        assert "Topics matched" not in out

    def test_stats_query_output_contains_mean(self, capsys):
        main(["calculate mean and statistics"])
        out = capsys.readouterr().out
        assert "Mean" in out


# ---------------------------------------------------------------------------
# format_response edge cases
# ---------------------------------------------------------------------------

class TestFormatResponseEdgeCases:
    def _make_response(self, **kwargs):
        defaults = dict(
            query="test",
            is_valid=True,
            topics_found=[],
            answer="Sample answer.",
            next_steps=[],
            error=None,
        )
        defaults.update(kwargs)
        return AgentResponse(**defaults)

    def test_no_next_steps_omits_section_header(self):
        resp = self._make_response(next_steps=[])
        text = format_response(resp)
        assert "Next Steps" not in text

    def test_multiple_next_steps_all_appear(self):
        steps = ["Step one.", "Step two.", "Step three."]
        resp = self._make_response(next_steps=steps, topics_found=["deployment"])
        text = format_response(resp)
        for step in steps:
            assert step in text

    def test_error_message_included_in_output(self):
        resp = self._make_response(
            is_valid=False,
            answer="",
            error="Query is too short.",
        )
        text = format_response(resp)
        assert "Query is too short." in text
