def max_Prime_Factors(n: int) -> int:
    if n < 2:
        return 0
    largest = -1
    for i in range(2, int(n**0.5) + 1):
        while n % i == 0:
            if is_prime(i):
                largest = i
            n //= i
    if n > 1 and is_prime(n):
        largest = n
    return largest

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True