from typing import List

def odd_position(nums: List[int]) -> bool:
    """
    Check if every odd index (1-based) contains an odd number.
    
    Args:
    nums (List[int]): A list of integers.
    
    Returns:
    bool: True if every odd index contains an odd number, False otherwise.
    """
    if len(nums) == 0:
        # If the list is empty, it's considered to have all indices as even,
        # so we return True.
        return True
    if len(nums) == 1:
        # If there's only one element, it's trivially true that it's at an even index,
        # so we return True.
        return True
    # Iterate over the list starting from index 1 and stepping by 2 (odd indices).
    for i in range(1, len(nums), 2):
        # Check if the current element at the odd index is even.
        if nums[i] % 2 == 0:
            # If any element at an odd index is even, return False.
            return False
    # If all elements at odd indices are odd, return True.
    return True
