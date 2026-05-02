# DIP392 – AI Study Assistant Agent

**RTU Course:** DIP392 – AI and Agent-Based Systems
**Practical Task:** System Implementation, Testing, and Deployment

---

## Project Title

AI Study Assistant Agent — a command-line AI agent that answers study questions using a local knowledge base.

---

## Task Description

Implement a small but complete AI/agent-based Python CLI system as part of the DIP392 practical task.
The system must demonstrate agent-based design, tool use, clean Python code, and a full test suite.

---

## System Goal

Help students quickly look up and understand study topics from the terminal.
The user types a topic or question; the agent processes it through a pipeline of tools and returns
a structured, readable answer with recommended next steps.

---

## AI / Agent-Based Approach

The system uses a **tool-using agent architecture** without any paid external AI API:

```
User Input
    │
    ▼
ValidatorTool        ← sanitizes and validates input
    │
    ▼
Intent Classification ← detects statistics vs. knowledge queries
    │
    ├──► CalculatorTool   (for statistics/math questions)
    │
    └──► SearchTool       (keyword search over knowledge base)
              │
              └──► FileReaderTool  (loads Markdown knowledge base)
    │
    ▼
Structured Answer + Next Steps
```

The agent follows the **Perception → Reasoning → Action → Output** pattern common to real AI agents.

---

## Tools Used

| Tool | Purpose |
|------|---------|
| `ValidatorTool` | Validates and sanitizes user input |
| `FileReaderTool` | Reads and parses the local Markdown knowledge base |
| `SearchTool` | Keyword-based relevance search over knowledge base sections |
| `CalculatorTool` | Arithmetic operations and descriptive statistics (mean, median, std dev) |

---

## Project Structure

```
dip392-ai-agent-practical/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   └── study_agent/
│       ├── __init__.py
│       ├── agent.py          ← StudyAssistantAgent class
│       ├── main.py           ← CLI entry point (argparse)
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── validator.py
│       │   ├── file_reader.py
│       │   ├── search_tool.py
│       │   └── calculator.py
│       └── data/
│           └── knowledge_base.md
├── tests/
│   ├── test_agent.py         ← 13 agent workflow tests
│   └── test_tools.py         ← 26 tool-level tests
└── docs/
    ├── journal_step_1.md
    ├── journal_step_2.md
    ├── submission_step_1_text.txt
    ├── submission_step_2_text.txt
    └── deployment_strategy.md
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/dip392-ai-agent-practical.git
cd dip392-ai-agent-practical

# (Optional) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## How to Run

```bash
# General knowledge query
python3 -m study_agent.main "testing and deployment"

# AI / agents query
python3 -m study_agent.main "explain AI agents and tools"

# Statistics query (uses CalculatorTool)
python3 -m study_agent.main "calculate mean and statistics"

# Verbose mode (shows matched topics)
python3 -m study_agent.main --verbose "Python programming"

# Help
python3 -m study_agent.main --help
```

---

## How to Test

```bash
python3 -m pytest tests/ -v
```

Expected output: **39 passed**.

To see test coverage:

```bash
python3 -m pytest tests/ --cov=src/study_agent --cov-report=term-missing
```

---

## GitHub / Deployment

See [`docs/deployment_strategy.md`](docs/deployment_strategy.md) for:
- Local setup steps
- Git branching strategy
- GitHub Actions CI/CD configuration
- How to extend the knowledge base and add new tools

The project is structured to be pushed directly to GitHub:

```bash
git remote add origin https://github.com/<your-username>/dip392-ai-agent-practical.git
git branch -M main
git push -u origin main
```

---

## Knowledge Base Topics

The local `data/knowledge_base.md` covers:
- Software Testing
- Deployment
- Artificial Intelligence
- Agents
- Python Programming
- Statistics
