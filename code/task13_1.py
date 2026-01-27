```python
import collections

def maximum_flow(n, edges):
    """
    Maximum Flow Problem

    A flow network is a directed graph which has a source (vertex 0) and a sink
    (vertex n-1). In a flow network, each edge (u, v) has a capacity c(u, v).
    Each edge receives a flow, but the amount of flow on the edge cannot exceed
    the corresponding capacity.

    Find the maximum flow from the source (vertex 0) to the sink (vertex n-1).

    This problem requires implementing a maximum flow algorithm such as:
    - Ford-Fulkerson with BFS (Edmonds-Karp algorithm)
    - Dinic's algorithm
    - Push-relabel algorithm

    The algorithm must:
    1. Build a residual graph from the input edges
    2. Repeatedly find augmenting paths from source to sink
    3. Update the residual capacities along the path
    4. Sum up all the flow pushed through augmenting paths

    Args:
        n: int - number of vertices (vertices numbered 0 to n-1)
                 source = 0, sink = n-1
        edges: list of tuples (u, v, c) - directed edges where:
               u = source vertex of edge
               v = destination vertex of edge
               c = capacity of edge (max flow allowed through this edge)

    Returns:
        int - the maximum flow from vertex 0 to vertex n-1

    Constraints:
        - 2 <= n <= 100
        - 1 <= |edges| <= 1000
        - 0 <= capacity <= 10000

    Example 1:
        Input:
            n = 4
            edges = [(0,1,2), (0,2,1), (1,2,1), (1,3,1), (2,3,2)]

        Graph visualization:
                 2
            0 -------> 1
            |          |  \
          1 |        1 |   \ 1
            v          v    v
            2 -------> 3 (sink)
                 2

        Output: 3

        Explanation:
        - Path 0->1->3 can carry flow of 1
        - Path 0->2->3 can carry flow of 1
        - Path 0->1->2->3 can carry flow of 1
        - Total maximum flow = 3

    Example 2:
        Input:
            n = 2
            edges = [(0,1,5)]
        Output: 5 (direct edge from source to sink)

    Example 3:
        Input:
            n = 5
            edges = [(0,1,10), (0,2,10), (1,3,4), (1,4,8), (2,4,9), (3,4,10)]
        Output: 19

    Note: This is a classic graph theory problem that requires understanding of:
    - Residual graphs and reverse edges
    - Augmenting paths
    - The max-flow min-cut theorem
    """
    graph = collections.defaultdict(dict)
    for u, v, c in edges:
        graph[u][v] = graph[u].get(v, 0) + c
        graph[v][u] = graph[v].get(u, 0)

    source = 0
    sink = n - 1
    max_flow = 0

    while True:
        parent = [-1] * n
        queue = collections.deque([source])
        parent[source] = source

        while queue:
            u = queue.popleft()
            for v, capacity in graph[u].items():
                if parent[v] == -1 and capacity > 0:
                    parent[v] = u
                    queue.append(v)
                    if v == sink:
                        break
            if parent[sink] != -1:
                break

        if parent[sink] == -1:
            break

        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        max_flow += path_flow

        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_
