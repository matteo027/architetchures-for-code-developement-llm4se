import math

def max_Prime_Factors(n: int) -> int:
    # Initialize the maximum prime factor variable
    max_prime = -1
    
    # Divide n by 2 to remove all even factors
    while n % 2 == 0:
        max_prime = 2
        n //= 2
    
    # n must be odd at this point, so a skip of 2 (i.e., i = i + 2) can be used
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        # While i divides n, update max_prime and divide n
        while n % i == 0:
            max_prime = i
            n //= i
    
    # If n is a prime number greater than 2, then n itself is the max prime factor
    if n > 2:
        max_prime = n
    
    return max_prime