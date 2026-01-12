from typing import List

def sort_matrix(M: List[List[int]]) -> List[List[int]]:
    return sorted(M, key=lambda row: sum(row))