def count_partitions(n: int) -> int:
    """Write a python function to count the number of ways to divide an integer 'n' into parts.
    The parts must sum to 'n'. Order does not matter (e.g., 1+2 is the same as 2+1).
    
    >>> count_partitions(5)
    7
    """
    if n < 0:
        return 0
    if n == 0:
        return 1

    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        for j in range(i, n + 1):
            dp[j] += dp[j - i]

    return dp[n]