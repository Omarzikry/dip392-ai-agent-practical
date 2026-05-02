# DIP392 – Practical Task Journal: Step 2

**Date:** 08.05.2025
**Student:** Omar Zikry
**Course:** DIP392 – AI and Agent-Based Systems

---

## 1. Updated System Description

The AI Study Assistant Agent has been fully implemented as planned. The system is a Python CLI tool
that users invoke with:

```
python -m study_agent.main "your topic or question"
```

The agent receives the query, validates it, classifies the intent, searches a local Markdown knowledge
base (or delegates to the statistics calculator), and returns a structured multi-section answer with
recommended study next steps.

All four tools are implemented and integrated. The test suite covers 39 test cases across both the
agent workflow and individual tools.

---

## 2. Refined List of Programming Concepts Actually Used

| Concept | Where Used |
|---------|-----------|
| Python dataclasses | `ValidationResult`, `SearchResult`, `StatsResult`, `AgentResponse` |
| Type hints | All function signatures, return types, `Optional[T]`, `list[T]`, `dict[K,V]` |
| OOP (classes, methods) | `StudyAssistantAgent`, `ValidatorTool`, `FileReaderTool`, `SearchTool`, `CalculatorTool` |
| Argparse | `main.py` – `build_parser()` function |
| pathlib.Path | `FileReaderTool` – resolves knowledge base path relative to package |
| String parsing / text processing | `SearchTool._extract_keywords()`, `SearchTool._score()` |
| Python `statistics` module | `CalculatorTool.describe()` – mean, median, stdev |
| Exception handling | `FileReaderTool.read()`, `CalculatorTool.divide()`, `CalculatorTool.describe()` |
| pytest | 39 tests across `test_agent.py` and `test_tools.py` |
| Modular package design | `src/study_agent/` package with `tools/` sub-package |
| Git version control | 7 meaningful commits documenting project evolution |

---

## 3. Explanation of How Concepts Are Applied

**Dataclasses** are used to define clean, typed return values for every tool and the agent itself.
Instead of returning raw dicts or tuples, each operation returns an object with named fields
(e.g. `AgentResponse.topics_found`, `StatsResult.mean`). This makes the code self-documenting
and easy to test.

**Type hints** appear on every function signature. They serve both as documentation and as
a contract that helps catch mistakes early during development.

**OOP / classes** separate concerns cleanly: the `StudyAssistantAgent` orchestrates but does
not implement tool logic. Each `*Tool` class is independently testable and replaceable.

**String processing** in `SearchTool` filters stop words, lower-cases keywords, then scores
each knowledge base section by keyword overlap — giving a simple but effective relevance
ranking without any external AI library.

**Statistics module** powers the `CalculatorTool.describe()` method, computing mean, median,
and standard deviation on a numeric list, demonstrating built-in library integration.

---

## 4. How Tools Are Integrated Into the Agent

The `StudyAssistantAgent.run()` method follows a clear four-step pipeline:

```
Input
  └─► ValidatorTool.validate()         (always called first)
        └─► [if invalid] → return error AgentResponse
        └─► [if valid]
              └─► classify intent (keyword check for stats triggers)
                    ├─► [stats] → CalculatorTool.describe() → format answer
                    └─► [knowledge] → SearchTool.search()
                                          └─► FileReaderTool.read_sections() (inside SearchTool)
                                               └─► rank sections → build answer → suggest next steps
```

The `SearchTool` internally uses `FileReaderTool` to parse the knowledge base on demand.
This keeps tool dependencies explicit and the agent code clean.

---

## 5. Testing Summary

- **39 tests** in `tests/test_agent.py` (13 tests) and `tests/test_tools.py` (26 tests).
- All 39 tests pass with `python3 -m pytest tests/ -v`.
- Coverage includes: valid queries, empty/short/long input, unknown topics, stats path,
  file-not-found, division by zero, empty list statistics, and more.
