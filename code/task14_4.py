def sort_matrix(M: List[List[int]]) -> List[List[int]]:
    """ Write a function to sort a given matrix in ascending order according to the sum of its rows. """
    row_sums = [sum(row) for row in M]
    sorted_pairs = sorted(zip(row_sums, M), key=lambda x: x[0])
    sorted_rows = [pair[1] for pair in sorted_pairs]
    return sorted_rows