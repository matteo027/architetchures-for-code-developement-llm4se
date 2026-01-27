import heapq
from typing import List, Tuple

def shortest_path(v: int, edges: List[Tuple[int, int, int]], start_node: int) -> List[int]:
    """
    Statement
    Given a weighted directed graph G(V, E) and a source node 'start_node'.
    Find the shortest path distance from 'start_node' to all other nodes.
    
    Input:
    - v: number of vertices (nodes are 0 to v-1)
    - edges: list of tuples (source, target, weight)
    - start_node: the index of the starting node
    
    Output:
    - Return a list of integers of size v, where the i-th element is the shortest distance from start_node to node i.
    - If a node is unreachable, return -1 for that node.
    """
    adj = [[] for _ in range(v)]
    for u, w, weight in edges:
        adj[u].append((w, weight))

    distances = [float('inf')] * v
    distances[start_node] = 0
    priority_queue = [(0, start_node)]

    while priority_queue:
        dist, u = heapq.heappop(priority_queue)

        if dist > distances[u]:
            continue

        for neighbor, weight in adj[u]:
            if distances[u] + weight < distances[neighbor]:
                distances[neighbor] = distances[u] + weight
                heapq.heappush(priority_queue, (distances[neighbor], neighbor))

    result = []
    for d in distances:
        if d == float('inf'):
            result.append(-1)
        else:
            result.append(d)
    return result