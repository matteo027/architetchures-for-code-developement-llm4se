from typing import List

def get_substring(a: int, b: int, c: int, d: int) -> str:
    """
    This function takes four integers as input and returns a substring of length 2 from the string formed by repeating 'A' a number of times equal to the first integer (a), followed by 'B' a number of times equal to the second integer (b). The function then returns the character at index c-1 up to but not including index d.

    Parameters:
    - a (int): The first integer that determines how many times 'A' should be repeated.
    - b (int): The second integer that determines how many times 'B' should be repeated.
    - c (int): The starting index for extracting the substring.
    - d (int): The ending index for extracting the substring.

    Returns:
    - str: A substring of length 2 from the string formed by repeating 'A' a number of times equal to the first integer (a), followed by 'B' a number of times equal to the second integer (b).
    """
    # Check if a is greater than b and swap them if necessary
    if a > b:
        a, b = b, a
    
    # Concatenate 'A' and 'B' strings based on the values of a and b
    res = 'A' * a + 'B' * b
    
    # Return the character at index c-1 up to but not including index d
    return res[c-1:d]
```