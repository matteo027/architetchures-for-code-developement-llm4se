from typing import List

def is_beautiful_poles(heights: List[int]) -> str:
    """
    Determines if a list of integers represents a beautiful poles configuration.
    
    A beautiful poles configuration is defined as follows:
    - The length of the list must be at least 3.
    - All elements in the list must be unique.
    - No element can be negative.
    - The sum of the first two elements should be twice the third element.
    
    Parameters:
    heights (List[int]): A list of integers representing the heights of poles.
    
    Returns:
    str: "YES" if the list represents a beautiful poles configuration, otherwise "NO".
    """
    # Check if the list has at least 3 elements
    if len(heights) < 3:
        return "Invalid input"
    
    # Check if all elements in the list are unique
    if len(set(heights)) != len(heights):
        return "Invalid input"
    
    # Check if there are any negative elements in the list
    if any(h < 0 for h in heights):
        return "Invalid input"
    
    # Extract the first three elements
    a, b, c = heights[0], heights[1], heights[2]
    
    # Check if the condition 2*b == a + c holds
    if 2 * b == a + c:
        return "YES"
    else:
        return "NO"