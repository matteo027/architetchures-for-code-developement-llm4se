from typing import List


def is_beautiful_poles(heights: List[int]) -> str:
    """Statement

Three poles stand evenly spaced along a line. Their heights are a, b and c
meters, from left to right. We will call the arrangement of the poles
_beautiful_ if the tops of the poles lie on the same line, that is, b-a = c-b.

Determine whether the arrangement of the poles is beautiful."""
    if len(heights) != 3:
        return "Invalid input: Exactly three heights are required."

    a, b, c = heights[0], heights[1], heights[2]

    if b - a == c - b:
        return "Beautiful"
    else:
        return "Not Beautiful"