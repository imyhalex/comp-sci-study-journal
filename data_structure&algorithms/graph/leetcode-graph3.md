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

## 2477. Minimum Fuel Cost to Report to the Capital[[Link](https://leetcode.com/problems/minimum-fuel-cost-to-report-to-the-capital/description/)]

```py
"""
Question Understading:
- Input:
    - `roads`: list of paird [a, b], where represents connected cities
        - undirected, no cycle
    - `seats`: int, maximum capacity of each car
    - `n`: number of cities (0-indexed, captital is citt 0)
- Rules:
    - Each city have one car
    - Represenattive can ride in car from another city
    - Moving along the edge costs 1 liter of fuel
- Output:
    - Minimum unit of fuel cost that let all representative to reach the captial (n = 0) 

Cases:
- n = 1, (only captical exists); ret = 0
- seats = 1, (everyone drive separately)
- seats >= n (everyone can fit in one car from the farthest)

Assumptions:
- 1 <= n <= 10^5
- 1 <= seats <= 10^5
- Roads must connect to the captial

Simple Operations:
- DFS, traverse from the captial
- Construct AdjList
- Count representatives in each subtree
- Compute the number of cars needed in each subtree
- Keep track of fuel have used in each subtree

Approach:
- Algo Analysis: Time: O(n); Space: O(n)
- Maintain:
    - `adj_list`: adjaceny list of graph
    - `fuel`: record fuel cost
- Steps:
    - After built adjancy list, do:
    - DFS travseral (dfs(node, parent))
        - Iterate through each child in subtree
            - get the repsentatives by calling dfs(child, node)
            - calculate the number of car needed
            - increment the `fuel` by adding number of car needed
            - update the total number of representative
        - Return total number of representatives from subtree
    - Return the final recorded fuel

"""

class Solution:
    def minimumFuelCost(self, roads: List[List[int]], seats: int) -> int:
        adj_list = defaultdict(list)

        for u, v in roads:
            adj_list[u].append(v)
            adj_list[v].append(u)
        
        self.fuel = 0
        
        def dfs(node, parent):
            reps = 1
            for child in adj_list[node]:
                if child != parent:
                    child_reps = dfs(child, node)
                    cars = math.ceil(child_reps / seats)
                    self.fuel += cars
                    reps += child_reps
            return reps
        
        dfs(0, -1)
        return self.fuel    
```

## 2492. Minimum Score of a Path Between Two Cities[[Link](https://leetcode.com/problems/minimum-score-of-a-path-between-two-cities/description/)]

```py
"""
Question Understanding:
- Input:
    - `n`: int from 1 to n, represents cities
    - `roads`: 2d array, each raods[i] in [a, b, distance], where
        - a , b two cities connected 
        - distance: the distance between two cities a and b
- Graph proerties:
    - undirected graph
- Output:
    - from the city 1 to the city n, keep track of minimal distatance (score), and return it

Clarifications:
- Does the graph have cycle?
- Can vertext in graph self connected?

Assumptions:
- 2 <= n <= 10^5
- 1 <= roads.length <= 10^5
- 1 <= a, b <= n
- 1 <= distance <= 10^5
- a != b

Cases:
- Only one road -> ret: that road distance

Simple Operations:
- BFS traverasal from city 1
- Keep track of reachable nodes
- Keep track of minimal distance 

Approach:
- Algo Analysis: Time: O(V + E); Space: o(V + E)
- Maintain:
    - Graph adjacency list
    - `visited` set
    - a global min_distance = `inf`
- Steps:
    - After built adj list
    - Do BFS traversal strating from city 1
    - For each edges encountered (u, v, w)
        - Update the min_distance = min(min_distance, w)
        - if the current v have not visited
            - add it to the `visited` set
            - put it itnto `q` for future opretaions
    - Return the min_distance
"""
class Solution:
    def minScore(self, n: int, roads: List[List[int]]) -> int:
        adj_list = defaultdict(list)
        for u, v, dist in roads:
            adj_list[u].append((v, dist))
            adj_list[v].append((u, dist))
        
        visited = set([1])
        q = deque([1])
        res = float('inf')

        while q:
            u = q.popleft()
            for v, dist in adj_list[u]:
                res = min(res, dist)
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        return res
```

## 1254. Number of Closed Islands[[Link](https://leetcode.com/problems/number-of-closed-islands/description/)]

```py
"""
Problem Understanding:
- Input:
    - A 2D grid of size m x n
    - grid[r][c] = 0 → land, grid[r][c] = 1 → water
- Output:
    - The number of closed islands
- Closed island:
    - An island of land cells completely surrounded by water
    - Cannot touch the grid’s border

Clarifying Questions:
- Can the grid be non-square? (Yes, m and n may differ)
- Can an island have holes inside it? (Yes, but still considered 1 island if connected by 0s)
- Do diagonals count as connections? (No, only 4 directions)

Assumptions:
- 1 <= m, n <= 100
- Grid contains only 0 and 1
- We count each group of connected 0s that does not touch border

Edge Cases:
- Entire grid is water → return 0
- Entire grid is land → return 0 (because touches border)
- Land only in middle → return 1
- Multiple small isolated islands in center → count all

Underlying Simple Operations:
- DFS/BFS flood-fill
- Boundary check
- Visited tracking

Brute Force Approach:
- For each cell, start DFS/BFS if it is land and not visited
- During DFS, check if it touches border
- If no border touch → count island
- Complexity: O(m*n)

My Approach & Design:
Approach:
- Algo Analysis: Time O(m*n), Space O(m*n) for visited
- Maintain:
    - visited set
    - dfs helper
    - res counter
- Steps:
    - Step 1: Flood-fill from border lands (0s on edge)
      - Reasoning: these cannot be closed, so mark them visited
    - Step 2: Traverse grid inside
      - If find unvisited land (0), run DFS
      - Increment result count
      - Reasoning: each DFS marks entire island
    - Step 3: Return count
"""
class Solution:
    def closedIsland(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        visited = set()

        def dfs(r, c):
            if (r < 0 or c < 0 or r == rows or c == cols
                or (r, c) in visited or grid[r][c]):
                return
            visited.add((r, c))
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        # Step 1: remove border islands
        for r in range(rows):
            for c in range(cols):
                if (r in [0, rows - 1] or c in [0, cols - 1]) and grid[r][c] == 0:
                    dfs(r, c)

        # Step 2: count closed islands
        res = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 0 and (r, c) not in visited:
                    dfs(r, c)
                    res += 1

        return res
```