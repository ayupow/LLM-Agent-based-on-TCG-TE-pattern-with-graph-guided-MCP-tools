# -*- coding: utf-8 -*-
"""Tool: median - Median value."""

def median(numbers: list) -> float:
    """Median value."""
    import statistics; return statistics.median(numbers) if numbers else 0
