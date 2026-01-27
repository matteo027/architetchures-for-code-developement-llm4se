from typing import List


def min_two_bells(prices: List[int]) -> int:
    """Statement

Snuke is buying a bicycle. The bicycle of his choice does not come with a
bell, so he has to buy one separately.

He has very high awareness of safety, and decides to buy two bells, one for
each hand.

The store sells three kinds of bells for the price of a, b and c yen (the
currency of Japan), respectively. Find the minimum total price of two
different bells."""
    prices.sort()
    return prices[0] + prices[1]
