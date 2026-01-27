import heapq
import math
from typing import List, Tuple

def shortest_path(v: int, edges: List[Tuple[int, int, int]], start_node: int) -> List[int]:
    """Finds shortest path distances from a start node in a weighted directed graph."""

    dist = [math.inf] * v
    dist[start_node] = 0

    adj = [[] for _ in range(v)]
    for u, target, weight in edges:
        adj[u].append((target, weight))

    pq = [(0, start_node)]

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue

        for neighbor, weight in adj[u]:
            # Relax edge: update distance if a shorter path is found.
            if dist[u] + weight < dist[neighbor]:
                dist[neighbor] = dist[u] + weight
                heapq.heappush(pq, (dist[neighbor], neighbor))

    # Mark unreachable nodes with -1.
    for i in range(v):
        if dist[i] == math.inf:
            dist[i] = -1

    return dist