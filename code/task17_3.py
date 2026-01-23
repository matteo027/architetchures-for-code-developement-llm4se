from typing import List 

def min_two_bells(prices: List[int]) -> int:
    """
    This function calculates the minimum price of two consecutive bells from a list of prices.
    
    Parameters:
    prices (List[int]): A list of integers representing the prices of different bells.
    
    Returns:
    int: The minimum price of two consecutive bells.
    """
    min_price = float('inf')  # Initialize the minimum price to infinity
    min_price_index = -1  # Initialize the index of the minimum price
    
    for i, price in enumerate(prices):  # Iterate through each price in the list
        if price not in prices[:i]:  # Check if the current price is not present before the current index
            min_price = min(min_price, price)  # Update the minimum price if the current price is smaller
            min_price_index = i  # Update the index of the minimum price
    
        elif i > min_price_index:  # If the current index is greater than the index of the minimum price
            min_price = min(min_price, price + min_price)  # Update the minimum price by adding the current price and the minimum price found before the current index
    
    return min_price  # Return the minimum price of two consecutive bells