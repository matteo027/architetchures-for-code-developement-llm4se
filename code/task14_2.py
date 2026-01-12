from typing import List

def sort_matrix(M: List[List[int]]) -> List[List[int]]:
    """
    Sorts a given matrix (list of lists of integers) based on the sum of its rows.
    
    Args:
    M (List[List[int]]): The input matrix to be sorted.
    
    Returns:
    List[List[int]]: The sorted matrix.
    """
    if not M:
        return []
    
    # Calculate the sum of each row
    row_sums = [sum(row) for row in M]
    
    # Sort the matrix based on the row sums
    sorted_matrix = [row for _, row in sorted(zip(row_sums, M))]
    
    return sorted_matrix