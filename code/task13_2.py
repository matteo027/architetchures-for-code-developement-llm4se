def make_palindrome(string: str) -> str:
    longest_palindrome_suffix = ''
    for i in range(len(string), 0, -1):
        if is_palindrome(string[i-1:]):
            longest_palindrome_suffix = string[i-1:]
            break
    prefix_to_add = string[:len(string)-len(longest_palindrome_suffix)]
    return longest_palindrome_suffix + prefix_to_add[::-1]