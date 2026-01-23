def is_palindrome(s: str) -> bool:
    return s == s[::-1]


def make_palindrome(string: str) -> str:
    if not string:
        return ''
    
    # Find the longest palindromic suffix
    for i in range(len(string)):
        suffix = string[i:]
        if is_palindrome(suffix):
            # Reverse the prefix (part before the palindromic suffix) and append
            prefix = string[:i]
            return string + prefix[::-1]
    
    return string