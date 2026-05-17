# Sensitive Info Validator

A Python command-line tool that helps users check text before sharing it by detecting possible sensitive or private information.

## Short Description

Paste or pipe text into the tool and it will scan for emails, phone numbers, API keys, card-like numbers, IP addresses, URLs, and other private values. It produces a clear report with each finding's category, position, risk level, and a redacted version of the original text.

## Planned Features

- Regex-based detection for common sensitive patterns (fast and deterministic)
- Gemini 1.5 Flash AI classification for ambiguous or context-dependent PII
- Heuristic fallback when no Gemini API key is configured
- Severity scoring (low / medium / high / critical)
- Automatic redaction of detected values
- Plain-text and JSON report output
- Reads from a file path argument or stdin

## Planned Architecture

```
sensitive_info_validator/
  main.py             – CLI entry point (argparse)
  agent_controller.py – sequential tool-use pipeline
  input_handler.py    – file / stdin reader
  models.py           – dataclasses for findings and results
  tools/
    regex_scanner.py    – pattern matching with re
    pii_classifier.py   – Gemini + heuristic fallback
    severity_scorer.py  – risk level assignment
    redactor.py         – value masking
    report_generator.py – plain-text / JSON output
tests/
  …unit and integration tests…
docs/
  journal_step1.md – planning
  journal_step2.md – implementation
  journal_step3.md – testing and refinement
  final_report_notes.md
```

## Development Plan

1. **Step 1 (current)** – Scaffold project structure, plan architecture, write journal.
2. **Step 2** – Implement all tools and the agent pipeline; add `.env` support for the Gemini key.
3. **Step 3** – Write unit and integration tests with pytest; refine edge cases.
4. **Final** – Polish CLI UX, complete documentation, submit.

> Implementation is not complete yet. This repository is under active development.
