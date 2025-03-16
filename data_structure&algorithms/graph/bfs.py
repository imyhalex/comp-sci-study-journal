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
    # adj = [[1], [0, 2, 3], [1], [1, 4], [3]]
    adj = [[2, 3, 1], [0], [0, 4], [0], [2]]
    src = 0
    graph = BFS(adj, src)
    ans = graph.bsf()
    for i in ans:
        print(i, end=' ')
    print()