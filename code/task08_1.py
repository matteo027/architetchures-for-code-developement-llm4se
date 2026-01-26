from typing import List


def is_odd_product(a: int, b: int) -> str:
    """Statement

You are given integers A and B, each between 1 and 3 (inclusive).

Determine if there is an integer C between 1 and 3 (inclusive) such that A
\times B \times C is an odd number."""
    for c in range(1, 4):
        if (a * b * c) % 2 != 0:
            return "Yes"
    return "No"
