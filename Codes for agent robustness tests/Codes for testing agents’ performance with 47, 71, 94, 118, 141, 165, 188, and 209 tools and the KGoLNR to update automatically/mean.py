# -*- coding: utf-8 -*-
"""Tool: mean - Arithmetic mean."""

def mean(numbers: list) -> float:
    """Arithmetic mean."""
    return sum(numbers) / len(numbers) if numbers else 0
