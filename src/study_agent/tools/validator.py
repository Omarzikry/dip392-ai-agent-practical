"""Input validation tool for the Study Assistant Agent."""

from dataclasses import dataclass


@dataclass
class ValidationResult:
    is_valid: bool
    cleaned_query: str
    message: str


class ValidatorTool:
    """Validates and sanitizes user input before processing."""

    MIN_LENGTH = 3
    MAX_LENGTH = 500

    def validate(self, query: str) -> ValidationResult:
        """Validate a user query string.

        Returns a ValidationResult with is_valid flag and cleaned text.
        """
        if not query or not query.strip():
            return ValidationResult(
                is_valid=False,
                cleaned_query="",
                message="Query is empty. Please provide a topic or question.",
            )

        cleaned = query.strip()

        if len(cleaned) < self.MIN_LENGTH:
            return ValidationResult(
                is_valid=False,
                cleaned_query=cleaned,
                message=f"Query is too short (minimum {self.MIN_LENGTH} characters).",
            )

        if len(cleaned) > self.MAX_LENGTH:
            return ValidationResult(
                is_valid=False,
                cleaned_query=cleaned[: self.MAX_LENGTH],
                message=f"Query is too long (maximum {self.MAX_LENGTH} characters). It has been truncated.",
            )

        return ValidationResult(
            is_valid=True,
            cleaned_query=cleaned,
            message="Input is valid.",
        )
