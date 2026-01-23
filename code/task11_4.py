from typing import List

def mean_absolute_deviation(numbers: List[float]) -> float:
    mean = sum(numbers) / len(numbers)
    total_diff = 0
    for num in numbers:
        total_diff += abs(num - mean)
    return total_diff / len(numbers)