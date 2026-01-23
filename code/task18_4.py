from typing import List

def is_beautiful_poles(heights: List[int]) -> str:
    """
    Determines if three given poles can form an equilateral triangle.
    
    Args:
    heights (List[int]): A list of integers representing the heights of the poles.
    
    Returns:
    str: "YES" if the poles can form an equilateral triangle, otherwise "NO".
    """
    # Check if the number of poles is exactly 3
    if len(heights) != 3:
        # If not, return "NO"
        return "NO"
    
    # Assign the heights to variables a, b, and c
    a, b, c = heights
    
    # Calculate the difference between consecutive poles
    diff_ab = b - a
    diff_bc = c - b
    
    # Check if the differences are equal
    if diff_ab == diff_bc:
        # If they are, return "YES"
        return "YES"
    else:
        # If they are not, return "NO"
        return "NO"