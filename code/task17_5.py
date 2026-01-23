from typing import List

def min_two_bells(prices: List[int]) -> int:
    """
    Calculate the minimum cost of buying two bells from a given list of prices.

    Args:
    prices (List[int]): A list of integers representing the prices of the bells.

    Returns:
    int: The minimum cost of buying two bells.

    Raises:
    ValueError: If the input list does not contain exactly three elements.
    """
    # Check if the input list contains exactly three elements
    if len(prices) != 3:
        raise ValueError("Input list must contain exactly three elements")

    # Calculate the minimum cost by comparing the sum of the first two and the second two bells
    return min(prices[0] + prices[1], prices[0] + prices[2], prices[1] + prices[2])
