def vowels_count(s):
    """Write a function vowels_count which takes a string representing
    a word as input and returns the number of vowels in the string.
    Vowels in this case are 'a', 'e', 'i', 'o', 'u'. Here, 'y' is also a
    vowel, but only when it is at the end of the given word.

    Example:
    >>> vowels_count("abcde")
    2
    >>> vowels_count("ACEDY")
    3
    >>> vowels_count("hello")
    2
    >>> vowels_count("rhythm")
    1
    >>> vowels_count("fly")
    1
    >>> vowels_count("MYTH")
    1
    >>> vowels_count("")
    0
    >>> vowels_count("bcdfgh")
    0
    >>> vowels_count("AEIOU")
    5
    >>> vowels_count("aEiOuY")
    6
    >>> vowels_count("y")
    1
    >>> vowels_count("Y")
    1
    >>> vowels_count("by")
    1
    >>> vowels_count("BY")
    1
    >>> vowels_count("why")
    1
    >>> vowels_count("WHY")
    1
    """
    vowels = "aeiouAEIOU"
    count = 0
    s_lower = s.lower()
    for i, char in enumerate(s_lower):
        if char in vowels:
            count += 1
        elif char == 'y' and i == len(s_lower) - 1:
            count += 1
    return count
