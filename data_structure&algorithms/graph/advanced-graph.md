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

# Kruskal's[[Link](https://neetcode.io/courses/advanced-algorithms/16)]

- find  minimum spanning tree

```python
# time: O(E log V); space: O(E)
class UnionFind:
    def __init__(self, n):
        self.par = {}
        self.rank = {}

        for i in range(1, n + 1):
            self.par[i] = i
            self.rank[i] = 0
    
    # Find parent of n, with path compression.
    def find(self, n):
        p = self.par[n]
        while p != self.par[p]:
            self.par[p] = self.par[self.par[p]]
            p = self.par[p]
        return p

    # Union by height / rank.
    # Return false if already connected, true otherwise.
    def union(self, n1, n2):
        p1, p2 = self.find(n1), self.find(n2)
        if p1 == p2:
            return False
        
        if self.rank[p1] > self.rank[p2]:
            self.par[p2] = p1
        elif self.rank[p1] < self.rank[p2]:
            self.par[p1] = p2
        else:
            self.par[p1] = p2
            self.rank[p2] += 1
        return True

# Given an list of edges of a connected undirected graph,
# with nodes numbered from 1 to n,
# return a list edges making up the minimum spanning tree.
def minimumSpanningTree(edges, n):
    min_heap = []
    for n1, n2, weight in edges:
        heapq.heappush(min_heap, [weight, n1, n2])
    
    union_find = UnionFind(n)
    mst = []
    while len(mst) < n - 1:
        weight, n1, n2 = heapq.heappop(min_heap)
        if not union_find.union(n1, n2):
            continue
        mst.append([n1, n2])
    return mst
```

# Topological Sort[[Link](https://neetcode.io/courses/advanced-algorithms/17)]

- only work on directed, acyclical graph
- graph does not have to be connected

```python
# postorder, reverse the result
# for cycle detection, use another hashset : path = set()

def dfs(src, adj_list, visited, top_sort):
    if src in visited:
        return True

    for neighbor in adj[src]:
        dfs(neigbhor, adj_list, visited, top_sort)
    visited.add(src)
    top_sort.append(src)

def topological_sort(edges, n):
    adj_list = {}
    for i in range(1, n + 1):
        adj_list[i] = []
    for src, dst in edges:
        adj_list[src].append(dst)
    
    top_sort = []
    visited = set()
    for i in range(1, n + 1):
        dfs(i, adj_list, visited, top_sort)
    top_sort.reverse()
    return top_sort
```