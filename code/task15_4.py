import math

def max_Prime_Factors(n: int) -> int:
    """
    This function calculates the largest prime factor of a given integer `n`.
    
    Parameters:
    - n (int): The integer to find the largest prime factor of.
    
    Returns:
    - int: The largest prime factor of `n`.
    """
    if n < 2:
        return 0
    largest_prime = 0
    # Iterate from 2 up to the square root of n
    for i in range(2, int(math.sqrt(n)) + 1):
        # While i divides n, update largest_prime and divide n
        while n % i == 0:
            largest_prime = i
            n //= i
    # If n is still greater than 1, it must be a prime number
    if n > 1:
        largest_prime = n
    return largest_prime