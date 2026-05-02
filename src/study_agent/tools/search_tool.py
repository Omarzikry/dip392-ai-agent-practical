"""Keyword search tool — finds relevant sections in the knowledge base."""

from dataclasses import dataclass, field
from typing import Optional

from .file_reader import FileReaderTool


@dataclass
class SearchResult:
    topic: str
    content: str
    relevance_score: float  # 0.0 – 1.0


class SearchTool:
    """Searches the knowledge base for sections matching user keywords."""

    def __init__(self, file_reader: Optional[FileReaderTool] = None) -> None:
        self.reader = file_reader or FileReaderTool()

    def search(self, query: str) -> list[SearchResult]:
        """Return knowledge base sections ranked by keyword overlap with query.

        Returns a list of SearchResult sorted by relevance (highest first).
        Returns an empty list when no section has any keyword match.
        """
        keywords = self._extract_keywords(query)
        if not keywords:
            return []

        sections = self.reader.read_sections()
        results: list[SearchResult] = []

        for topic, content in sections.items():
            score = self._score(keywords, topic, content)
            if score > 0:
                results.append(SearchResult(topic=topic, content=content, relevance_score=score))

        results.sort(key=lambda r: r.relevance_score, reverse=True)
        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _extract_keywords(self, query: str) -> list[str]:
        """Lower-case all words, strip punctuation, drop short stop words."""
        stop_words = {
            "a", "an", "the", "is", "are", "was", "were", "in", "on",
            "at", "to", "of", "for", "and", "or", "but", "with", "how",
            "what", "why", "when", "where", "who", "explain", "describe",
            "tell", "me", "about", "give", "some", "can", "you",
        }
        words: list[str] = []
        for word in query.lower().split():
            clean = "".join(ch for ch in word if ch.isalnum())
            if clean and clean not in stop_words and len(clean) > 2:
                words.append(clean)
        return words

    def _score(self, keywords: list[str], topic: str, content: str) -> float:
        """Calculate a simple overlap score between keywords and section text."""
        text = (topic + " " + content).lower()
        matches = sum(1 for kw in keywords if kw in text)
        # Bonus weight for a keyword found directly in the topic heading
        topic_bonus = sum(0.5 for kw in keywords if kw in topic.lower())
        raw = matches + topic_bonus
        return round(raw / max(len(keywords), 1), 4)
