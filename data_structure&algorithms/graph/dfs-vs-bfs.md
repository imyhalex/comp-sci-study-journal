# Depth First Traversal for a Graph

- Time Complexity: O(V + E)
    - visit every vertex at most once and every edge is traversed at most once (in directed) and twice in undirected.
- Auxiliray Space: O(V + E)
    - extra visited array of size V is required
    - And stack size for recursive calls to DFSRec function
- Traverse all adjacent verticesd one by one
- Completly finish the traversal of all vertices
- Graph may contain cycles
    - Leads to a node visted more than once
    - Need to use a boolean visted arrray to avoid this

## Example
```text
Note : There can be multiple DFS traversals of a graph according to the order in which we pick adjacent vertices. Here we pick vertices as per the 
insertion order.

1.
Input: adj =  [[1, 2], [0, 2], [0, 1, 3, 4], [2], [2]] -> transalte to edges = [[0, 1], [0, 2], [1, 2], [2, 3], [2, 4]]

Output: 1 0 2 3 4
Explanation:  The source vertex s is 1. We visit it first, then we visit an adjacent. 
Start at 1: Mark as visited. Output: 1
Move to 0: Mark as visited. Output: 0 (backtrack to 1)
Move to 2: Mark as visited. Output: 2 (backtrack to 0)
Move to 3: Mark as visited. Output: 3 (backtrack to 2)
Move to 4: Mark as visited. Output: 4 (backtrack to 2)


Not that there can be more than one DFS Traversals of a Graph. For example, after 1, we may pick adjacent 2 instead of 0 and get a different DFS. Here we pick in the insertion order.

2.
Input: [[2,3,1], [0], [0,4], [0], [2]]

Output: 0 2 4 3 1
Explanation: DFS Steps:

Start at 0: Mark as visited. Output: 0
Move to 2: Mark as visited. Output: 2
Move to 4: Mark as visited. Output: 4 (backtrack to 2, then backtrack to 0)
Move to 3: Mark as visited. Output: 3 (backtrack to 0)
Move to 1: Mark as visited. Output: 1
```

## Implementation (Undirected & Unweighted)
```python
class DFS:
    def __init__(self, V, edges):
        self.V = V
        self.adj = [[] for _ in range(V)]
        self.edges = edges
        for e in self.edges:
            self.add_edge(e[0], e[1])

    def add_edge(self, s, t):
        self.adj[s].append(t)
        self.adj[t].append(s)

    def dfs_rec(self, node, visited, result):
        visited[node] = True
        result.append(node)

        for neighbor in self.adj[node]:
            if not visited[neighbor]:
                self.dfs_rec(neighbor, visited, result)
    
    def dfs(self, start):
        visited = [False] * self.V
        result = []

        self.dfs_rec(start, visited, result)
        return result

if __name__ == "__main__":
    # adj =  [[1, 2], [0, 2], [0, 1, 3, 4], [2], [2]]
    edges = [[0, 1], [0, 2], [1, 2], [2, 3], [2, 4]]
    V = 5
    graph = DFS(V, edges)

    # Start DFS from vertex 1
    dfs_result = graph.dfs(1)
    print("DFS Traversal:", dfs_result)
```

## Implementation (Undirected & Unweighted, but Disconnected)
```python
class DFS:
    def __init__(self, V, edges):
        """Initializes the graph with V vertices and given edges."""
        self.V = V
        self.adj = [[] for _ in range(V)]
        self.edges = edges
        for e in self.edges:
            self.add_edge(e[0], e[1])

    def add_edge(self, s, t):
        """Adds an undirected edge between s and t."""
        self.adj[s].append(t)
        self.adj[t].append(s)

    def dfs_rec(self, node, visited, result):
        """Recursive DFS traversal."""
        visited[node] = True
        result.append(node)

        for neighbor in self.adj[node]:
            if not visited[neighbor]:
                self.dfs_rec(neighbor, visited, result)

    def dfs_disconnected(self):
        """Handles disconnected graphs by running DFS on each component."""
        visited = [False] * self.V
        all_components = []

        for v in range(self.V):  # Ensure all vertices are visited
            if not visited[v]:  
                component = []  # Stores the current connected component
                self.dfs_rec(v, visited, component)
                all_components.append(component)

        return all_components  # List of all DFS traversals (one per component)

# Example Usage
if __name__ == "__main__":
    # Example: Disconnected graph
    edges = [[0, 1], [0, 2], [3, 4]]  # Two separate components: {0,1,2} and {3,4}
    V = 5
    graph = DFS(V, edges)

    # Perform DFS on the entire disconnected graph
    dfs_result = graph.dfs_disconnected()
    print("DFS Traversal for Each Component:", dfs_result)
```

# Breadth First Traversal for a Graph

- Time Copmplexity O(V + E):
    - BFS explores all the vertices and edges in the graph
    - Worst case: visits every vertex and edge once
    - V and E are the number of vertices and edges in the given graph
- Auxiliray Space: O(V):
    - BFS use queue to keep track of the vertices that need to be visited
    - Worst case: queue can contain all the vertices in the graph
- Starting from Vertex 0
- Visting vertices from left to right accoding to the adjacency list
- return list containing the BFS traversal of the graph

## Example
```text
1.
Input: adj = [[2,3,1], [0], [0,4], [0], [2]]

Output: [0, 2, 3, 1, 4]
Explanation: Starting from 0, the BFS traversal will follow these steps: 
Visit 0 → Output: 0 
Visit 2 (first neighbor of 0) → Output: 0, 2 
Visit 3 (next neighbor of 0) → Output: 0, 2, 3 
Visit 1 (next neighbor of 0) → Output: 0, 2, 3, 
Visit 4 (neighbor of 2) → Final Output: 0, 2, 3, 1, 4

2.
Input: adj = [[1, 2], [0, 2], [0, 1, 3, 4], [2], [2]]

Output: [0, 1, 2, 3, 4]
Explanation: Starting from 0, the BFS traversal proceeds as follows: 
Visit 0 → Output: 0 
Visit 1 (the first neighbor of 0) → Output: 0, 1 
Visit 2 (the next neighbor of 0) → Output: 0, 1, 2 
Visit 3 (the first neighbor of 2 that hasn’t been visited yet) → Output: 0, 1, 2, 3 
Visit 4 (the next neighbor of 2) → Final Output: 0, 1, 2, 3, 4

3.
Input: adj = [[1], [0, 2, 3], [1], [1, 4], [3]]

Output: [0, 1, 2, 3, 4]
Explanation: Starting the BFS from vertex 0:
Visit vertex 0 → Output: [0]
Visit vertex 1 (first neighbor of 0) → Output: [0, 1]
Visit vertex 2 (first unvisited neighbor of 1) → Output: [0, 1, 2]
Visit vertex 3 (next neighbor of 1) → Output: [0, 1, 2, 3]
Visit vertex 4 (neighbor of 3) → Final Output: [0, 1, 2, 3, 4]
```

## Implementation (Undirected & Unweighted)

__approach__
1. Initialization: Enqueue the given source vertex into a queue and mark it as visited
2. Exploration: While the queue is not empty
    - Dequeue a node from the queue and visit it
    - For each unvisted neighbor of the dequeued node (under the condition of visted check):
        - enqueue the neighbor into the queue
        - mark the neighbor as visited

```python
from collections import deque

class BFS:
    def __init__(self, adj, s):
        self.adj = adj
        self.s = s
    
    def bsf(self):
        # get the number of vertices
        V = len(self.adj)

        # initialize
        ans = []
        visited = [False] * V
        q = deque()

        visited[self.s] = True
        q.append(self.s)

        while q:
            curr = q.popleft()
            ans.append(curr)

            for neighbor in self.adj[curr]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    q.append(neighbor)
        return ans


if __name__ == "__main__":
    adj = [[2, 3, 1], [0], [0, 4], [0], [2]]
    src = 0
    graph = BFS(adj, src)
    ans = graph.bsf()
    for i in ans:
        print(i, end=' ')
```

## Implementation (Undirected & Unweighted, but Disconnected)
```python
from collections import deque

class BFS:
    def __init__(self, adj):
        self.adj = adj
        self.V = len(adj)  # Number of vertices

    def bfs(self, start, visited):
        """Performs BFS from a given start node."""
        q = deque()
        q.append(start)
        visited[start] = True
        result = []

        while q:
            curr = q.popleft()
            result.append(curr)

            for neighbor in self.adj[curr]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    q.append(neighbor)

        return result

    def bfs_disconnected(self):
        """Handles BFS traversal for a disconnected graph."""
        visited = [False] * self.V
        all_components = []  # Stores BFS results for each component

        for v in range(self.V):  # Loop through all vertices
            if not visited[v]:  # Start BFS for an unvisited component
                component = self.bfs(v, visited)
                all_components.append(component)

        return all_components
        
# Example Usage
if __name__ == "__main__":
    # Example: Disconnected graph
    adj = [[2, 3, 1], [0], [0, 4], [0], [2], [6], [5]]  # Two separate components: {0,1,2,3,4} and {5,6}
    
    graph = BFS(adj)
    bfs_result = graph.bfs_disconnected()

    print("BFS Traversal for Each Component:", bfs_result)
```