# -*- coding: utf-8 -*-
"""Tool: mode - Most common value."""

def mode(numbers: list) -> float:
    """Most common value."""
    import statistics; return statistics.mode(numbers) if numbers else 0
