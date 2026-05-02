"""File reader tool — loads the local knowledge base into memory."""

from pathlib import Path
from typing import Optional


class FileReaderTool:
    """Reads a Markdown knowledge base file and returns its contents."""

    def __init__(self, knowledge_base_path: Optional[Path] = None) -> None:
        if knowledge_base_path is None:
            # Default path relative to this file's package location
            knowledge_base_path = Path(__file__).parent.parent / "data" / "knowledge_base.md"
        self.path = Path(knowledge_base_path)

    def read(self) -> str:
        """Read and return the full knowledge base content.

        Raises FileNotFoundError if the knowledge base file is missing.
        """
        if not self.path.exists():
            raise FileNotFoundError(f"Knowledge base not found at: {self.path}")
        return self.path.read_text(encoding="utf-8")

    def read_sections(self) -> dict[str, str]:
        """Parse the knowledge base into a dict keyed by top-level heading.

        Returns a mapping of heading -> section body text.
        """
        content = self.read()
        sections: dict[str, str] = {}
        current_heading: Optional[str] = None
        buffer: list[str] = []

        for line in content.splitlines():
            if line.startswith("## "):
                if current_heading is not None:
                    sections[current_heading] = "\n".join(buffer).strip()
                current_heading = line[3:].strip().lower()
                buffer = []
            else:
                buffer.append(line)

        if current_heading is not None:
            sections[current_heading] = "\n".join(buffer).strip()

        return sections
