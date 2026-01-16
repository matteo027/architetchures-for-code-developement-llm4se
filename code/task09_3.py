def get_substring(a: int, b: int, c: int, d: int) -> str:
    """
    This function takes four integers as input and returns a string based on specific conditions.
    
    Parameters:
    a (int): The first integer.
    b (int): The second integer.
    c (int): The third integer.
    d (int): The fourth integer.
    
    Returns:
    str: A string representing the result of the conditions applied to the input integers.
    """
    # Check if either a or b is zero
    if a == 0 or b == 0:
        return ""
    
    # Check if the sum of a and b is odd
    if (a + b) % 2 == 1:
        return "A" * a + "B" * b
    
    # Determine which integer is greater and which is smaller
    if a > b:
        return "A" * (a - 1) + "B" * (b + 1)
    else:
        return "A" * (a + 1) + "B" * (b - 1)