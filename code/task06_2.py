from typing import List


def odd_position(nums: List[int]) -> bool:
    """ Write a python function to check whether every odd index contains odd numbers of a given list. """

    for i in range(len(nums)):
        if i % 2 != 0:  # Check if the index is odd
            if nums[i] % 2 == 0:  # Check if the number at the odd index is even
                return False
    return True
