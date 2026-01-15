from typing import List

def can_form_1974(digits: List[int]) -> str:
    """
    Determines if a given list of digits can form the number 1974.
    
    Args:
    digits (List[int]): A list of integers representing the digits to check.
    
    Returns:
    str: "YES" if the digits can form 1974, otherwise "NO".
    """
    # Sort the digits in ascending order
    sorted_digits = sorted(digits)
    
    # Check if the sorted digits match the sequence [1, 4, 7, 9]
    if sorted_digits == [1, 4, 7, 9]:
        return "YES"
    else:
        return "NO"
