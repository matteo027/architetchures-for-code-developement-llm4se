from typing import List
import statistics

def mean_absolute_deviation(numbers: List[float]) -> float:
    """
    Calculate the Mean Absolute Deviation (MAD) of a list of numbers.
    
    The MAD is a measure of variability that represents the average distance between each data point and the mean.
    
    Parameters:
    numbers (List[float]): A list of floating-point numbers.
    
    Returns:
    float: The Mean Absolute Deviation of the input numbers.
    
    Examples:
    >>> mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    1.0
    >>> mean_absolute_deviation([1.5, 2.5, 3.5, 4.5])
    1.0
    >>> mean_absolute_deviation([])
    0.0
    """
    if not numbers:
        return 0.0
    # Calculate the mean of the numbers
    mean = statistics.mean(numbers)
    # Calculate the absolute differences from the mean
    abs_diffs = [abs(x - mean) for x in numbers]
    # Calculate the mean of these absolute differences
    mad = statistics.mean(abs_diffs)
    return mad