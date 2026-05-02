# DIP392 – Practical Task Journal: Step 1

**Date:** 24.04.2025
**Student:** Omar Zikry
**Course:** DIP392 – AI and Agent-Based Systems

---

## 1. Planned System and Goal

**System name:** AI Study Assistant Agent

**Goal:** Build a small command-line AI agent that helps students look up and understand study topics. The user types a question or topic into the terminal; the agent processes it, searches a local knowledge base, and returns a structured, readable answer with recommended next steps.

The system is designed to be:
- Self-contained (no external API keys required).
- Clearly agent-based (the agent orchestrates tools in a defined workflow).
- Simple enough to explain during a student defense.

---

## 2. AI / Agent-Based Approach

The system follows a **tool-using agent architecture**:

1. **Input arrives** at the agent via the CLI.
2. The agent **validates** the input with a Validator tool.
3. The agent **classifies** the intent (general knowledge lookup vs. statistics/calculation).
4. The agent **selects and calls** the appropriate tool(s):
   - `SearchTool` for knowledge base lookups.
   - `CalculatorTool` for statistics/math questions.
5. The agent **synthesises** a structured text response and presents it to the user.

This mimics real agent patterns (perception → reasoning → action → output) without relying on a remote LLM API.

---

## 3. List of Planned Tools

| Tool | Purpose |
|------|---------|
| `ValidatorTool` | Validates and sanitizes user input before processing |
| `FileReaderTool` | Reads the local Markdown knowledge base into memory |
| `SearchTool` | Searches knowledge base sections by keyword relevance |
| `CalculatorTool` | Provides arithmetic and descriptive statistics operations |

---

## 4. Preliminary List of Programming Concepts Required

- **Python OOP** – classes, methods, dataclasses, inheritance.
- **Type hints** – function signatures with `str`, `list`, `dict`, `Optional`, etc.
- **Argparse** – command-line interface argument parsing.
- **File I/O** – reading Markdown files with `pathlib`.
- **String processing** – splitting, filtering stop words, keyword scoring.
- **Statistics** – mean, median, standard deviation via the `statistics` module.
- **Exception handling** – `FileNotFoundError`, `ValueError` with meaningful messages.
- **pytest** – unit testing with assertions, fixtures, and edge-case coverage.
- **Modular design** – separating agent logic from tool implementations.
- **Git version control** – committing in meaningful increments.
