from typing import List


def min_two_bells(prices: List[int]) -> int:
    if len(prices) < 2:
        return 0

    min_price = float('inf')
    min_price_index = -1

    for i, price in enumerate(prices):
        if i == 0 or price != prices[i-1]:
            if price < min_price:
                min_price = price
                min_price_index = i

    if min_price_index == -1:
        return 0

    second_min_price = float('inf')
    for i, price in enumerate(prices):
        if i != min_price_index and price < second_min_price:
            second_min_price = price

    return min_price + second_min_price