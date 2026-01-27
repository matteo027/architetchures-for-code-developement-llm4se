from typing import List


def min_two_bells(prices: List[int]) -> int:
    """Finds the sum of the two smallest bell prices.

    Args:
        prices: A list of integer bell prices.

    Returns:
        The sum of the two smallest prices.
    """
    prices.sort()
    # After sorting, the two smallest prices are at the beginning of the list.
    return prices[0] + prices[1]
