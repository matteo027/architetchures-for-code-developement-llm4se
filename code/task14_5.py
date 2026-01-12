def sort_matrix(M: List[List[int]]) -> List[List[int]]:
    """Write a function to sort a given matrix in ascending order according to the sum of its rows."""
    sums = [sum(row) for row in M]
    sorted_pairs = sorted(zip(sums, M), key=lambda x: (x[0], tuple(x[1])))
    sorted_rows = [pair[1] for pair in sorted_pairs]
    return sorted_rows