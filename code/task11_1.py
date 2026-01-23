from typing import List

def mean_absolute_deviation(numbers: List[float]) -> float:
    mean = sum(numbers) / len(numbers)
    return sum(abs(x - mean) for x in numbers) / len(numbers)

# Example usage
print(mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]))  # Output: 1.0