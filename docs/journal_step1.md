# Step 1 Journal – Planning

## 1. System Goal

The planned system is a Python-based Sensitive-info Text Validator. Its goal is to help users check text before sharing it by detecting possible sensitive or private information. The system can identify values such as email addresses, phone numbers, bank/card-like numbers, API keys, URLs, IP addresses, and other private values.

The problem it solves is accidental exposure of private or confidential information in documents, messages, reports, or code snippets. This can create privacy, security, or compliance risks.

The main users are students, developers, office workers, and anyone who needs to review text before sending, uploading, or publishing it.

The expected outcome is a clear report showing detected sensitive data, its category, position, risk level, explanation, and a redacted version of the original text.

## 2. AI or Agent-Based Approach

The system uses a single intelligent agent that follows a sequential tool-use pipeline. The agent receives input text and decides which tools to call in order. First, it calls a Regex Scanner for predictable sensitive patterns. Then, ambiguous findings are passed to a Gemini-based PII Classifier. After classification, the agent calls a Severity Scorer, then a Redaction Tool, and finally a Report Generator.

This is better than using only an LLM because structured values such as emails, IP addresses, URLs, and API keys can be detected quickly and deterministically with regex. The LLM is used only where context is needed, such as ambiguous numbers or possible private values in natural language.

## 3. Planned Tools

- **Regex Scanner** – Receives raw text; returns a list of pattern matches with type, value, and position.
- **Gemini PII Classifier** – Receives ambiguous text snippets; returns a classification label and confidence score. Falls back to heuristics when no API key is available.
- **Severity Scorer** – Receives classified findings; returns each finding annotated with a severity level (low / medium / high / critical).
- **Redaction Tool** – Receives original text and a list of findings; returns a redacted version with sensitive values replaced by placeholders.
- **Report Generator** – Receives scored and redacted findings; returns a formatted plain-text or JSON report.
- **File/Input Reader** – Receives a file path or reads from stdin; returns the raw text string for processing.

## 4. Preliminary Programming Concepts

- **Python modules and packages** – Code is organised into files (modules) grouped under directories with `__init__.py` (packages), enabling reusable imports.
- **Functions** – Named, reusable blocks of code that accept parameters and return values; the building block of each tool.
- **Dataclasses** – Python classes decorated with `@dataclass` that auto-generate `__init__` and other methods; used to represent findings and results with typed fields.
- **Regular expressions** – Patterns written in the `re` module syntax that efficiently match structured text like emails, phone numbers, and IP addresses.
- **Lists and dictionaries** – Core collection types; lists hold ordered findings, dictionaries map keys to values for structured results and configuration.
- **JSON formatting** – The `json` module serialises Python objects to a human-readable, machine-parseable format for report output.
- **File handling** – The built-in `open()` function reads text from files; combined with stdin support for flexible input.
- **Environment variables** – Loaded via `python-dotenv`; keep secrets like the Gemini API key out of source code.
- **Error handling** – `try/except` blocks handle missing API keys, unreadable files, and unexpected input gracefully.
- **Unit testing with pytest** – Test functions prefixed with `test_` are discovered and run by pytest; ensures each tool behaves correctly in isolation.
- **Git version control** – Commits track each meaningful change; branches and history allow rollback and collaboration.
