def make_palindrome(string: str) -> str:
    """
    Create the shortest palindrome by appending characters to the given string.

    Strategy:
    ---------
    A palindrome reads the same forwards and backwards. To turn any string
    into a palindrome with minimal additions, we look for the longest tail
    (suffix) that is already symmetric. Whatever comes before that tail
    must be mirrored and tacked onto the end.

    Example walkthrough with 'cat':
        - Check if 'cat' is a palindrome → No
        - Check if 'at' is a palindrome  → No
        - Check if 't' is a palindrome   → Yes (single char)
        - Prefix before 't' is 'ca', reversed = 'ac'
        - Result: 'cat' + 'ac' = 'catac'
    """
    if not string:
        return ''

    # Scan from index 0 forward; the first suffix that mirrors itself wins.
    for start in range(len(string)):
        suffix = string[start:]
        if suffix == suffix[::-1]:
            prefix = string[:start]
            return string + prefix[::-1]

    # Fallback (though a single-char suffix always matches above)
    return string