## 1129. Shortest Path with Alternating Colors[[Link](https://leetcode.com/problems/shortest-path-with-alternating-colors/description/)]

- video explaination[[Link](https://neetcode.io/solutions/shortest-path-with-alternating-colors)]

```py
"""
Question Understanding:
- Input:
    - An integer `n` representing number of nodes labeled from `0` to `n - 1`.
    - `redEdges`: list of directed edges [a, b] with red color (a → b).
    - `blueEdges`: list of directed edges [u, v] with blue color (u → v).
- Graph:
    - Directed, may have self-edges, may have multiple edges
    - Edges can be red or blue
- Output:
    - An integer array answer of size n
        - answer[x] = shortest path length from node 0 to node x
        - Path must alternate edge colors (red → blue → red or blue → red → blue)
        - If no valid alternating path, answer[x] = -1

Clarifying Questions:
1. Can there be multiple edges of the same color between the same nodes? (Yes, allowed per problem statement)
2. Can a node have both red and blue self-edges? (Yes, possible)
3. Is the path length defined as number of edges? (Yes)
4. Do we start from node 0 without a color constraint? (Yes, first edge can be either red or blue)

Assumptions:
- n ≥ 1
- redEdges and blueEdges contain valid nodes 0 ≤ u, v < n
- answer[0] = 0 always (distance from node 0 to itself)
- Graph size constraints: n ≤ 100 (per LeetCode)

Edge Cases:
- n = 1 → output [0]
- No edges at all → only node 0 is reachable, rest -1
- Only red or only blue edges
- Cycles in graph (must ensure BFS avoids infinite loop)
- Self-edges (ignored if not useful for alternating path)
- Parallel edges of same/different color

Underlying Simple Operations:
- Store adjacency list separately for red and blue edges
- Maintain BFS queue with state (node, color, distance)
- Alternate color when exploring neighbors
- Track visited[(node, color)] to prevent revisiting
- Update answer[node] when first reached

Brute Force Approach:
- For each node x, run DFS from node 0 and try all alternating color paths
- Keep track of path lengths, pick minimum
- Complexity: O(n * (number of paths)) → exponential in worst case
- Not feasible for n=100

My Approach & Design (BFS with state):
Approach:
- Algo Analysis: Time O(n + redEdges + blueEdges), Space O(n + edges)
- Variables:
    - redAdj, blueAdj → adjacency lists
    - ans[n] → initialize with -1, ans[0] = 0
    - visited set → to avoid reprocessing (node, color)
    - queue for BFS → (node, color, distance)
- Maintain:
    - Start BFS with (0, red, 0) and (0, blue, 0)
    - BFS level by level
- Steps:
    1. Build adjacency lists:
        - Reasoning: Separate red and blue to quickly access next neighbors by color
    2. Initialize queue with both colors from node 0:
        - Reasoning: First step can be either red or blue
    3. BFS loop:
        - Pop (node, color, dist)
        - If ans[node] == -1 → update ans[node] = dist
            - Reasoning: first time reaching node guarantees shortest path
        - Explore neighbors of opposite color:
            - Reasoning: must alternate color
        - For each neighbor:
            - If (neighbor, nextColor) not visited:
                - Push into queue
                - Mark visited
    4. End BFS, return ans
"""

class Solution:
    def shortestAlternatingPaths(self, n: int, redEdges: List[List[int]], blueEdges: List[List[int]]) -> List[int]:
        blue_adj = defaultdict(list)
        red_adj = defaultdict(list)
        for u, v in redEdges:
            red_adj[u].append(v)
        for u, v in blueEdges:
            blue_adj[u].append(v)

        ans = [-1] * n
        ans[0] = 0

        # BFS queue: (node, color, distance)
        # color: 0=red, 1=blue
        q = deque([(0, 0, 0), (0, 1, 0)])
        visited = set([(0, 0), (0, 1)])

        while q:
            node, color, dist = q.popleft()

            # update the shortest distance
            if ans[node] == -1:
                ans[node] = dist
            else:
                ans[node] = min(ans[node], dist)

            # next color must alternate 
            # the last color was red
            if color == 0:
                for nei in blue_adj[node]:
                    if (nei, 1) not in visited:
                        visited.add((nei, 1))
                        q.append((nei, 1, dist + 1))
            else:
                for nei in red_adj[node]:
                    if (nei, 0) not in visited:
                        visited.add((nei, 0))
                        q.append((nei, 0, dist + 1))
            
        return ans
```