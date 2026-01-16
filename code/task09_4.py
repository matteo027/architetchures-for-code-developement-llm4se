from typing import List


def get_substring(a: int, b: int, c: int, d: int) -> str:
    """
    Generates a string f(A, B) and extracts a substring from c to d (1-based).
    
    Parameters:
    - a (int): The number of 'A' characters.
    - b (int): The number of 'B' characters.
    - c (int): The starting index of the substring (1-based).
    - d (int): The ending index of the substring (1-based).
    
    Returns:
    - str: The extracted substring from c to d.
    """
    # Generate the string f(A, B)
    result = []
    total_length = a + b
    while a > 0 or b > 0:
        # Determine which character to append based on the remaining length
        if a > b:
            result.append('A')
            a -= 1
        elif b > a:
            result.append('B')
            b -= 1
        else:
            # If both remain equal, decide which one to append first
            if not result or result[-1] == 'B':
                result.append('A')
                a -= 1
            else:
                result.append('B')
                b -= 1
    # Convert list to string
    f_ab = ''.join(result)
    # Extract the substring from c to d (1-based)
    return f_ab[c-1:d]