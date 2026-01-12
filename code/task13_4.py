def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]

def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string.

    Algorithm idea:
    - Find the longest suffix of the string that is already a palindrome.
    - Append to the end the reverse of the prefix before that suffix.

    >>> make_palindrome('')
    ''
    >>> make_palindrome('cat')
    'catac'
    >>> make_palindrome('cata')
    'catac'
    """
    if not string:
        return ''

    for i in range(len(string), 0, -1):
        suffix = string[-i:]
        if suffix == suffix[::-1]:
            prefix = string[:-i]
            return string + prefix[::-1]

    return string