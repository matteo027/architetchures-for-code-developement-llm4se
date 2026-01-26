from typing import Tuple


def longest_common_subsequence(a: str, b: str) -> int:
    """Calculates the length of the longest common subsequence between two strings."""
    n = len(a)
    m = len(b)

    # dp[i][j] will store the length of the LCS of a[:i] and b[:j]
    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                # If characters match, extend the LCS from the previous diagonal state
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # If characters don't match, take the maximum LCS from excluding either character
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]