import math

def max_Prime_Factors(n: int) -> int:
    """ 
    Write a python function to find the largest prime factor of a given number. 
    
    Parameters:
    - n (int): The input number for which the largest prime factor is to be found.
    
    Returns:
    - int: The largest prime factor of the given number.
    
    Raises:
    - ValueError: If the input is not a positive integer.
    """
    if n <= 0:
        raise ValueError("Input must be a positive integer.")
    if n == 1:
        return 1

    largest_prime_factor = 1

    # Check for smallest prime factor 2
    while n % 2 == 0:
        largest_prime_factor = 2
        n //= 2

    # Check for odd factors from 3 onwards
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            largest_prime_factor = i
            n //= i

    # If n is still greater than 2, then it is prime
    if n > 2:
        largest_prime_factor = n

    return largest_prime_factor