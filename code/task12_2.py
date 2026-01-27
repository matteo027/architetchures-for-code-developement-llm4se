def vowels_count(s):
    """Counts the number of vowels in a given string, treating 'y' as a vowel at the end of a word."""
    vowel_count = 0
    lower_s = s.lower()
    vowels = "aeiou"

    for char in lower_s:
        if char in vowels:
            vowel_count += 1

    if s and lower_s[-1] == 'y':
        # 'y' is treated as a vowel only when it appears at the end of the string.
        # It's not included in the initial `vowels` set, so this condition explicitly adds it.
        vowel_count += 1

    return vowel_count
