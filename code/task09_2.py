from typing import List


def get_substring(a: int, b: int, c: int, d: int) -> str:
    if a == 0 or b == 0:
        return ""

    total_length = a + b
    if total_length % 2 == 0 and a > b:
        return "A" * a + "B" * b

    if total_length % 2 == 1 and a > b:
        return "A" * a + "B" * b + "A"

    result = []
    i = 0
    while a > 0 and b > 0:
        if i % 2 == 0:
            result.append('A')
            a -= 1
        else:
            result.append('B')
            b -= 1
        i += 1

    if a > 0:
        result.extend(['A'] * a)
    elif b > 0:
        result.extend(['B'] * b)

    # Ensure the longest substring of equal letters is minimized
    if len(result) > 1:
        min_len = min(a, b)
        for j in range(len(result) - min_len):
            if result[j] == result[j + min_len]:
                result[j + min_len] = 'B' if result[j] == 'A' else 'A'

    return ''.join(result)[c-1:d]