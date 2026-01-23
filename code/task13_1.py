def make_palindrome(s):
    """
    Build the shortest palindrome by appending characters to the end of s.

    The algorithm identifies the longest suffix of s that is already a
    palindrome. Once found, only the prefix preceding that suffix needs
    to be reversed and appended to complete the palindrome.

    Args:
        s: Input string.

    Returns:
        A palindrome formed by s plus the minimal reversed prefix.
    """
    for i in range(len(s), 0, -1):
        if s[-i:] == s[-i:][::-1]:
            return s + s[:-i][::-1]
    return s
