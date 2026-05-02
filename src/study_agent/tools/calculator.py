"""Calculator / statistics helper tool."""

import statistics
from dataclasses import dataclass
from typing import Union


@dataclass
class StatsResult:
    count: int
    mean: float
    median: float
    std_dev: float
    minimum: float
    maximum: float


class CalculatorTool:
    """Provides basic arithmetic and descriptive statistics operations."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b

    def percentage(self, part: float, total: float) -> float:
        """Return what percentage `part` is of `total`."""
        if total == 0:
            raise ValueError("Total must not be zero.")
        return round((part / total) * 100, 2)

    def describe(self, values: list[Union[int, float]]) -> StatsResult:
        """Compute descriptive statistics for a list of numeric values."""
        if not values:
            raise ValueError("Cannot compute statistics on an empty list.")
        if len(values) == 1:
            v = float(values[0])
            return StatsResult(count=1, mean=v, median=v, std_dev=0.0, minimum=v, maximum=v)

        return StatsResult(
            count=len(values),
            mean=round(statistics.mean(values), 4),
            median=round(statistics.median(values), 4),
            std_dev=round(statistics.stdev(values), 4),
            minimum=min(values),
            maximum=max(values),
        )
