from typing import List, Tuple

class DSU:
    """Disjoint Set Union data structure for efficient set operations."""
    def __init__(self, n):
        """Initializes DSU with n elements, each in its own set."""
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i):
        """Finds the representative of the set containing element i with path compression."""
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """Unites the sets containing elements i and j using union by rank."""
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False

def kruskal_mst(v: int, edges: List[Tuple[int, int, int]]) -> int:
    """Computes the Minimum Spanning Tree (MST) weight using Kruskal's algorithm."""
    if v == 0:
        return 0

    edges.sort(key=lambda item: item[2])

    dsu = DSU(v)
    mst_weight = 0
    edges_count = 0

    for u, w, weight in edges:
        if dsu.union(u, w):
            mst_weight += weight
            edges_count += 1
            if edges_count == v - 1:
                break

    # Kruskal's algorithm naturally handles disconnected graphs by forming MSTs for each component.
    # The accumulated mst_weight represents the sum of weights of these component MSTs.

    return mst_weight