from typing import List

def count_colors(colors: List[int]) -> int:
    """Statement

AtCoDeer the deer recently bought three paint cans. The color of the one he
bought two days ago is a, the color of the one he bought yesterday is b, and
the color of the one he bought today is c. Here, the color of each paint can
is represented by an integer between 1 and 100, inclusive.

Since he is forgetful, he might have bought more than one paint can in the
same color. Count the number of different kinds of colors of these paint cans
and tell him."""
    return len(set(colors))