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