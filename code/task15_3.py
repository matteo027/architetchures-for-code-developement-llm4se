from math import sqrt

def is_prime(n: int) -> bool:
    if n == 1 or n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    max_divisor = sqrt(n)
    for d in range(3, int(max_divisor) + 1, 2):
        if n % d == 0:
            return False
    return True

def max_prime_factors(n: int) -> int:
    if n == 1:
        return 1
    if n < 0 or n == 0:
        raise ValueError("Invalid input")

    largest_prime_factor = 1

    while n % 2 == 0:
        largest_prime_factor = 2
        n /= 2

    max_divisor = int(sqrt(n))
    for d in range(3, max_divisor + 1, 2):
        while n % d == 0:
            largest_prime_factor = d
            n /= d

    if n > 2:
        largest_prime_factor = n

    return largest_prime_factor