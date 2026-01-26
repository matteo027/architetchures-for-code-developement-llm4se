from typing import List


def count_colors(colors: List[int]) -> int:
    """Counts the number of unique colors in a list.

    Args:
        colors: A list of integers representing colors.

    Returns:
        The total count of distinct colors.
    """
    unique_colors = set()
    for color in colors:
        unique_colors.add(color)
    return len(unique_colors)