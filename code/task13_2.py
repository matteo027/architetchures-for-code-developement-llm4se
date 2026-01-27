import collections

def maximum_flow(n, edges):
    """Computes the maximum flow in a network using the Edmonds-Karp algorithm.

    Args:
        n: The number of vertices in the graph (0-indexed).
        edges: A list of tuples, where each tuple is (u, v, capacity) representing
               a directed edge from vertex u to vertex v with the given capacity.

    Returns:
        The maximum flow from vertex 0 (source) to vertex n-1 (sink).
    """

    # Initialize a residual graph representation.
    # Adjacency list where each entry stores (destination, capacity, reverse_edge_index)
    graph = collections.defaultdict(list)
    for u, v, c in edges:
        graph[u].append([v, c, len(graph[v])])
        graph[v].append([u, 0, len(graph[u]) - 1]) # Reverse edge with 0 initial capacity

    total_flow = 0

    # While an augmenting path exists from the source (vertex 0) to the sink (vertex n-1)
    while True:
        # Find an augmenting path using Breadth-First Search (BFS).
        parent = [-1] * n
        parent_edge_index = [-1] * n
        queue = collections.deque([0])
        parent[0] = 0 # Source is its own parent to mark as visited

        while queue:
            u = queue.popleft()

            for i, (v, capacity, _) in enumerate(graph[u]):
                if parent[v] == -1 and capacity > 0:
                    parent[v] = u
                    parent_edge_index[v] = i
                    if v == n - 1: # Sink reached
                        break
                    queue.append(v)
            if parent[n - 1] != -1: # Sink reached, break outer loop
                break

        # If no path is found, break the loop.
        if parent[n - 1] == -1:
            break

        # Determine the bottleneck capacity of this path.
        path_flow = float('inf')
        s = n - 1
        while s != 0:
            p = parent[s]
            edge_idx = parent_edge_index[s]
            path_flow = min(path_flow, graph[p][edge_idx][1])
            s = p

        # Add the bottleneck capacity to the total flow.
        total_flow += path_flow

        # Update the residual capacities along the augmenting path.
        v = n - 1
        while v != 0:
            u = parent[v]
            edge_idx = parent_edge_index[v]
            reverse_edge_idx = graph[u][edge_idx][2]

            graph[u][edge_idx][1] -= path_flow
            graph[v][reverse_edge_idx][1] += path_flow
            v = u

    # Return the total flow.
    return total_flow
