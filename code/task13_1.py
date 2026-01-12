on
def make_palindrome(s):
    """
    This function takes a string `s` and returns the longest palindrome that can be formed by appending characters to the end of `s`.
    
    The function works as follows:
    1. It iterates over the string from the end to the beginning.
    2. For each character, it checks if the substring starting from that character is equal to its reverse.
    3. If such a substring is found, it appends the reverse of this substring to the original string `s` and returns the result.
    4. If no such substring is found after checking all possible substrings, it simply returns the original string `s`.
    
    Parameters:
    - s (str): The input string to form the palindrome from.
    
    Returns:
    - str: The longest palindrome that can be formed by appending characters to the end of `s`.
    """
    for i in range(len(s), 0, -1):
        if s[-i:] == s[-i:][::-1]:
            return s + s[:-i][::-1]
    return s
```