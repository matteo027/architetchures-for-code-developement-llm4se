from typing import List


def odd_position(nums: List[int]) -> bool:
    result = True
    for i in range(len(nums)):
        if i % 2 != 0:
            if nums[i] % 2 == 0:
                result = False
    return result
