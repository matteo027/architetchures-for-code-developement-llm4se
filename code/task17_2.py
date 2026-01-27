def count_partitions(n: int) -> int:
    """Counts the number of ways to partition an integer 'n' into positive integer parts.

    The order of parts does not matter. For example, partitions of 5 include:
    5, 4+1, 3+2, 3+1+1, 2+2+1, 2+1+1+1, 1+1+1+1+1.

    Args:
        n: The integer to partition.

    Returns:
        The number of distinct partitions of 'n'.

    >>> count_partitions(5)
    7
    """
    if n < 0:
        return 0

    dp = [0] * (n + 1)
    dp[0] = 1

    # Dynamic programming approach: dp[j] stores the number of ways to form sum 'j'.
    # The outer loop iterates through possible part sizes 'i'.
    # The inner loop updates dp[j] by considering partitions that include 'i'.
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            dp[j] += dp[j - i]

    return dp[n]