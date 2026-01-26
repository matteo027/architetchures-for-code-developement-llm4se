from typing import List


def is_beautiful_poles(heights: List[int]) -> str:
    """Checks if three pole heights form an arithmetic progression."""
    if len(heights) != 3:
        return "invalid input"
    a, b, c = heights
    diff1 = b - a
    diff2 = c - b
    # The condition for a "beautiful" set of poles is that the difference
    # between consecutive heights is constant, forming an arithmetic progression.
    if diff1 == diff2:
        return "YES"
    else:
        return "NO"