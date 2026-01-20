from typing import List


def min_two_bells(prices: List[int]) -> int:
    if len(prices) < 3:
        raise ValueError("The list must contain exactly three elements.")
    a, b, c = prices
    return min(a + b, a + c, b + c)