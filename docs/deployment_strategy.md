# Deployment Strategy – AI Study Assistant Agent

## Overview

This document describes how the AI Study Assistant Agent is packaged, tested, and deployed.

---

## Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/dip392-ai-agent-practical.git
cd dip392-ai-agent-practical

# 2. (Optional) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the agent
python3 -m study_agent.main "testing and deployment"

# 5. Run the test suite
python3 -m pytest tests/ -v
```

---

## GitHub Deployment

### Repository Structure

The project follows a standard Python repository layout:

```
dip392-ai-agent-practical/
  src/study_agent/      ← source package
  tests/                ← pytest test suite
  docs/                 ← journals and deployment notes
  requirements.txt
  README.md
  .gitignore
```

### Git Branching Strategy

For a student/educational project:
- `master` (or `main`) — stable, working code only.
- Feature branches: `feature/<name>` → merge via pull request.
- All merges to `master` should have passing tests.

### CI/CD with GitHub Actions (recommended next step)

Create `.github/workflows/ci.yml`:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
```

This runs the test suite automatically on every push.

---

## Environment Considerations

| Item | Detail |
|------|--------|
| Python version | 3.9 or higher (uses `dict[K,V]` type hint syntax in `file_reader.py`) |
| External dependencies | Only `pytest` and `pytest-cov` (dev-only) |
| External APIs | None — fully self-contained |
| Data | Local `data/knowledge_base.md` — no database required |

---

## Extending the System

To add a new knowledge topic:
1. Open `src/study_agent/data/knowledge_base.md`.
2. Add a new `## topic name` section with content.
3. The `SearchTool` will automatically pick it up — no code changes needed.

To add a new tool:
1. Create `src/study_agent/tools/my_tool.py` with a class.
2. Export it from `tools/__init__.py`.
3. Inject it into `StudyAssistantAgent.__init__()`.
4. Add a test in `tests/test_tools.py`.
