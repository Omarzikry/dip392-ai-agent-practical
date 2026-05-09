# DIP392 – Practical Task Journal: Step 3

**Date:** 15.05.2025
**Student:** Omar Zikry
**Course:** DIP392 – AI and Agent-Based Systems

---

## 1. Testing Process

Testing was performed continuously alongside implementation. Tests were written before or immediately
after each feature was added, following a Test-Driven Development (TDD) mindset where practical.

The test suite is organized into three files:

| File | Focus | Tests |
|------|-------|-------|
| `tests/test_tools.py` | Unit tests for each tool class | 26 |
| `tests/test_agent.py` | Agent workflow unit tests | 13 |
| `tests/test_integration.py` | Multi-component integration tests | 27 |
| `tests/test_cli.py` | CLI entry point and output format tests | 17 |
| **Total** | | **83** |

All tests are run with:

```bash
python3 -m pytest tests/ -v
```

Result: **83 passed** in under 0.15 seconds.

---

## 2. Test Scenarios

### 2.1 Happy-Path (Normal Workflow) Tests

| Scenario | What is Verified |
|----------|-----------------|
| Valid topic query (`"software testing"`) | Agent returns `is_valid=True`, non-empty answer, matching topic |
| Multi-keyword query (`"deployment strategies CI CD"`) | At least one next step is returned |
| Broad AI query | At least one knowledge base section is matched |
| Query echo in answer | The cleaned query text appears in the formatted answer string |
| TOP_K cap | No more than 3 topics are returned regardless of how many keywords match |

### 2.2 Statistics / Calculator Path Tests

| Scenario | What is Verified |
|----------|-----------------|
| Query contains `"mean"` | Routes to `CalculatorTool`; answer includes "Mean" |
| Query contains `"std"` | Routes to `CalculatorTool`; answer includes "Std Dev" |
| Stats answer contains numeric values | Demo dataset values (e.g. `72`) appear in output |
| Next steps are study-oriented | At least one suggestion mentions "statistic" or "variance" |

### 2.3 Invalid Input Tests

| Scenario | What is Verified |
|----------|-----------------|
| Empty string `""` | `is_valid=False`, `error` is set, `answer` is empty |
| Whitespace only `"    "` | Rejected before any tool is called |
| Single character `"a"` | Rejected by `ValidatorTool` (below MIN_LENGTH) |
| Two characters `"AI"` | Rejected (below MIN_LENGTH of 3) |
| Query over 500 characters | Rejected with truncation message |

### 2.4 No Knowledge Base Match Tests

| Scenario | What is Verified |
|----------|-----------------|
| Gibberish query (`"zgkqmplxtvw"`) | `topics_found=[]`, fallback message returned |
| Unrelated real-word query | Fallback message suggests known topics (testing, agents, etc.) |

### 2.5 Data Flow Between Tools Tests

| Scenario | What is Verified |
|----------|-----------------|
| Validator output feeds SearchTool | Cleaned query is passed unchanged; results are non-empty |
| FileReaderTool sections format | Returns `dict[str, str]` with non-empty values |
| SearchResult relevance scores | All scores are positive floats in valid range |
| CalculatorTool describe output | Returns typed `StatsResult` dataclass with correct values |

### 2.6 CLI Entry Point Tests

| Scenario | What is Verified |
|----------|-----------------|
| Valid query → exit code 0 | `main(["software testing"])` returns 0 |
| Empty argv → exit code 1 | `main([])` returns 1 |
| Whitespace query → exit code 1 | Whitespace-only string returns 1 |
| Invalid short query → exit code 1 | Two-char query returns 1 |
| Unknown topic → exit code 0 | No match is a handled result, not a crash |
| `--verbose` flag adds topics line | Printed output contains "Topics matched" |
| Without `--verbose` omits topics | "Topics matched" does not appear |
| Stats query prints "Mean" | Statistics output visible in stdout |

### 2.7 Error Handling Tests

| Scenario | What is Verified |
|----------|-----------------|
| Missing knowledge base file | `FileReaderTool.read()` raises `FileNotFoundError` |
| Division by zero | `CalculatorTool.divide(5, 0)` raises `ValueError` |
| Empty list to `describe()` | `CalculatorTool.describe([])` raises `ValueError` |
| Zero total in `percentage()` | `CalculatorTool.percentage(5, 0)` raises `ValueError` |

---

## 3. Deployment Preparation

### How to Run the System

```bash
# 1. Clone the repository
git clone https://github.com/omarzikry/dip392-ai-agent-practical.git
cd dip392-ai-agent-practical

# 2. Create a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .                  # install as editable package

# 4. Run the CLI agent
python3 -m study_agent.main "software testing"
python3 -m study_agent.main --verbose "explain AI agents"

# 5. Run all 83 tests
python3 -m pytest tests/ -v
```

### Dependencies

All dependencies are listed in `requirements.txt`:

```
pytest>=8.0
pytest-cov
fastapi
uvicorn[standard]
```

No external AI APIs are required. The system is fully self-contained.

### Environment Variables

No environment variables are required for the CLI version. The FastAPI backend reads the optional
`PORT` variable for the server port (default: 8000).

### GitHub Actions CI

A workflow is configured at `.github/workflows/ci.yml`. On every push or pull request to `main`,
GitHub automatically:
1. Installs Python 3.9 and 3.11
2. Installs all dependencies
3. Runs the full test suite (`python -m pytest tests/ -v`)

This ensures the system remains testable and deployable after every change.

---

## 4. Data Conversion and Porting

### Input Format

The user provides a plain-text string (via CLI argument or HTTP POST body).

### Data Transformation Steps

| Step | Transformation | Module |
|------|---------------|--------|
| 1 | Raw string → stripped, validated string | `ValidatorTool.validate()` |
| 2 | Validated string → list of keyword strings (stop words removed) | `SearchTool._extract_keywords()` |
| 3 | Keywords + Markdown file → `dict[str, str]` (topic → content) | `FileReaderTool.read_sections()` |
| 4 | Dict sections + keywords → list of `SearchResult` objects (sorted by score) | `SearchTool.search()` |
| 5 | `SearchResult` list → multi-line formatted answer string | `StudyAssistantAgent._build_answer()` |
| 6 | `AgentResponse` dataclass → CLI-printable text or JSON-serializable dict | `format_response()` / `api.py` |

### Format Consistency

Each tool returns a typed Python dataclass (`ValidationResult`, `SearchResult`, `StatsResult`,
`AgentResponse`). These act as typed contracts between components, preventing format mismatches
and making data flow explicit and testable.

The FastAPI backend converts `AgentResponse` to JSON using `response.dict()` (Pydantic-style)
so the same Python objects serve both CLI and web clients without duplication.
