from typing import List

def range_add_range_sum(n: int, queries: List[List[int]]) -> List[int]:
    """
    Range Add Range Sum Query (Segment Tree with Lazy Propagation)

    Implement a data structure that supports the following operations on an
    array A of n integers, all initially set to 0:

    1. add(s, t, x): Add x to all elements A[s], A[s+1], ..., A[t] (1-indexed)
    2. getSum(s, t): Return the sum A[s] + A[s+1] + ... + A[t] (1-indexed)

    This problem requires implementing a Segment Tree with Lazy Propagation
    to achieve O(log n) time complexity for both operations.

    The key insight is that when we need to update a range, we don't update
    all individual elements. Instead, we store "lazy" values at segment tree
    nodes that represent pending updates to propagate to children.

    Args:
        n: int - size of the array (1 <= n <= 100,000)
        queries: list of tuples - each query is one of:
            (0, s, t, x) - add x to elements from index s to t (inclusive, 1-indexed)
            (1, s, t) - return sum of elements from index s to t (inclusive, 1-indexed)

    Returns:
        list of int - results for each getSum query (type 1)

    Constraints:
        - 1 <= n <= 100,000
        - 1 <= q <= 100,000 (number of queries)
        - 1 <= s <= t <= n
        - -10,000 <= x <= 10,000

    Example:
        Input:
            n = 3
            queries = [
                (0, 1, 2, 1),   # add 1 to A[1..2]: A = [1, 1, 0]
                (0, 2, 3, 2),   # add 2 to A[2..3]: A = [1, 3, 2]
                (0, 3, 3, 3),   # add 3 to A[3..3]: A = [1, 3, 5]
                (1, 1, 2),      # sum A[1..2] = 1 + 3 = 4
                (1, 2, 3)       # sum A[2..3] = 3 + 5 = 8
            ]
        Output: [4, 8]

    Example 2:
        Input:
            n = 5
            queries = [
                (0, 1, 5, 1),   # add 1 to all: A = [1,1,1,1,1]
                (1, 1, 5),      # sum = 5
                (0, 2, 4, 2),   # add 2 to A[2..4]: A = [1,3,3,3,1]
                (1, 1, 5),      # sum = 11
                (1, 2, 4)       # sum = 9
            ]
        Output: [5, 11, 9]

    Implementation Notes:
        - Use a segment tree of size 4*n to be safe
        - Each node stores: sum of its range, lazy value (pending add)
        - Before accessing children, propagate lazy value down (push_down)
        - After updating children, recalculate parent sum (push_up)
        - The lazy propagation ensures O(log n) per operation
    """
    tree = [0] * (4 * n)
    lazy = [0] * (4 * n)

    def push_down(node: int, l: int, r: int):
        """Propagates lazy updates down the segment tree."""
        if lazy[node] != 0:
            mid = (l + r) // 2
            # Apply lazy value to children's tree nodes, scaled by their range size.
            tree[node * 2] += lazy[node] * (mid - l + 1)
            lazy[node * 2] += lazy[node]
            tree[node * 2 + 1] += lazy[node] * (r - mid)
            lazy[node * 2 + 1] += lazy[node]
            lazy[node] = 0

    def push_up(node: int):
        """Updates the current node's value based on its children."""
        tree[node] = tree[node * 2] + tree[node * 2 + 1]

    def update_range(node: int, l: int, r: int, s: int, t: int, x: int):
        """Adds a value x to all elements in the range [s, t] within the segment tree."""
        if s > r or t < l:
            return
        if s <= l and r <= t:
            tree[node] += x * (r - l + 1)
            lazy[node] += x
            return
        push_down(node, l, r)
        mid = (l + r) // 2
        update_range(node * 2, l, mid, s, t, x)
        update_range(node * 2 + 1, mid + 1, r, s, t, x)
        push_up(node)

    def query_sum(node: int, l: int, r: int, s: int, t: int) -> int:
        """Queries the sum of elements in the range [s, t] within the segment tree."""
        if s > r or t < l:
            return 0
        if s <= l and r <= t:
            return tree[node]
        push_down(node, l, r)
        mid = (l + r) // 2
        return query_sum(node * 2, l, mid, s, t) + query_sum(node * 2 + 1, mid + 1, r, s, t)

    results = []
    for query in queries:
        query_type = query[0]
        if query_type == 0:
            s, t, x = query[1], query[2], query[3]
            update_range(1, 1, n, s, t, x)
        elif query_type == 1:
            s, t = query[1], query[2]
            results.append(query_sum(1, 1, n, s, t))
    return results
