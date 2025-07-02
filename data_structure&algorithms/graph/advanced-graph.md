# Dijkstra's (shortest path)[[Link](https://neetcode.io/courses/advanced-algorithms/14)]

- Q: starting from A, find the length of the shortest path to evry other node
- Having already covered BFS, we will now cover another shortest path algorithm - Dijkstra's algorithm. 
    - The downside of using BFS is that it only works when the graph is unweighted - i.e. where the default weight of each edge is 1
    - Dijkstra's algo assumes no negative weight

```python
# Given a connected graph represented by a list of edges, where
# edge[0] = src, edge[1] = dst, and edge[2] = weight,
# find the shortest path from src to every other node in the 
# graph. There are n nodes in the graph.
# O(E * logV), O(E * logE) is also correct.

def shortestPath(edges, n, src):
    adj = {}
    for i in range(1, n + 1):
        adj[i] = []
        
    # s = src, d = dst, w = weight
    for s, d, w in edges:
        adj[s].append((d, w)) # node, weight

    shortest = {}
    minHeap = [(0, src)] # weight, node
    while minHeap:
        w1, n1 = heapq.heappop(minHeap)
        if n1 in shortest:
            continue
        shortest[n1] = w1

        for n2, w2 in adj[n1]: # mind the example code adj list store in reverse of min heap
            if n2 not in shortest:
                heapq.heappush(minHeap, (w1 + w2, n2))
    return shortest
```

# Prim's[[Link](https://neetcode.io/courses/advanced-algorithms/15)]

- find minimum spanning tree in undirected graph
- the graph is connected
- cannot have any cycle

```python
# O(E * logV), O(E * logE) is also correct.

# Given a list of edges of a connected undirected graph,
# with nodes numbered from 1 to n,
# return a list edges making up the minimum spanning tree.
def minimumSpanningTree(edges, n):
    adj = {}
    for i in range(1, n + 1):
        adj[i] = []

    for n1, n2, weight in edges:
        adj[n1].append([n2, weight])
        adj[n2].append([n1, weight])
    
    min_heap = []
    for neighbor, weight in adl[1]:
        heapq.heappush(min_heap, [weight, 1, neighbor])
    
    print(adj)
    mst = []
    visited = set()
    visited.add(1)
    while min_heap:
        weight, src, node = heapq.heappop(min_heap)
        if node in visited:
            continue
        
        mst.append([src, node])
        visited.add(node)
        for neighbor, weight in adk[node]:
            if neighbor not in visited:
                heapq.heappush(min_heap, [weight, node, neighbor])
    return mst
```