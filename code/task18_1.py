from typing import List, Tuple

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
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
    """
    Calculate the sum of weights of the Minimum Spanning Tree (MST) for a weighted undirected graph.
    
    Input:
    - v: number of vertices (0 to v-1)
    - edges: list of (source, target, weight)
    
    Output:
    - Total weight of the MST.
    """
    edges.sort(key=lambda item: item[2])
    
    ds = DisjointSet(v)
    mst_weight = 0
    num_edges = 0
    
    for u, v_node, weight in edges:
        if ds.union(u, v_node):
            mst_weight += weight
            num_edges += 1
            if num_edges == v - 1:
                break
    
    if num_edges != v - 1 and v > 1:
        return -1 # Indicates graph is not connected
    
    return mst_weight