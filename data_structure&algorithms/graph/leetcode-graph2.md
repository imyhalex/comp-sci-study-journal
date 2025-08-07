## 997. Find the Town Judge[[Link](https://leetcode.com/problems/find-the-town-judge/description/)]

- video explaination[[Link](https://neetcode.io/problems/find-the-town-judge?list=neetcode250)]

```python
# time: O(V + E); space: O(V)
class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        incoming = defaultdict(int)
        outgoing = defaultdict(int)

        for src, dst in trust:
            incoming[dst] += 1
            outgoing[src] += 1
        
        for i in range(1, n + 1):
            if incoming[i] == n - 1 and outgoing[i] == 0:
                return i
        
        return -1
```

## 286. Walls and Gates[[Link](https://leetcode.com/problems/walls-and-gates/description/)]

- video explaination[[Link](https://neetcode.io/problems/islands-and-treasure?list=neetcode250)]


## 1091. Shortest Path in Binary Matrix[[Link](https://leetcode.com/problems/shortest-path-in-binary-matrix/)]

- video explaination[[Link](https://neetcode.io/solutions/shortest-path-in-binary-matrix)]

```python
class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        if grid[0][0] != 0 or grid[rows - 1][cols - 1] != 0:
            return -1

        visited = set()
        q = deque()

        q.append((0, 0))
        visited.add((0, 0))

        length = 1 # start a (0, 0) counts as step 1
        while q:
            for i in range(len(q)): # take a snapshot of the length of the q
                r, c = q.popleft()
                if r == rows - 1 and c == cols - 1:
                    return length
                
                # view current r, c as [0, 0]
                neighbors = [
                    [1, 0], [-1, 0], [0, 1], [0, -1]
                    , [1, 1], [-1, 1], [1, -1], [-1, -1]
                ] # this is bascially directions
                for dr, dc in neighbors:
                    if (r + dr < 0 or c + dc < 0 or 
                        r + dr == rows or c + dc == cols or
                        (r + dr, c + dc) in visited or grid[r + dr][c + dc] == 1):
                        continue
                    q.append((r + dr, c + dc))
                    visited.add((r + dr, c + dc))
            length += 1
        
        return -1   
```

## 994. Rotting Oranges[[Link](https://leetcode.com/problems/rotting-oranges/description/)]

- video explaination[[Link](https://neetcode.io/problems/rotting-fruit)]
- dont need set `visited` becasue modify the grid in-place
- `while q and fresh > 0`:

```python
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        q = deque()
        fresh = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    fresh += 1
                if grid[r][c] == 2:
                    q.append((r, c))

        time = 0
        while q and fresh > 0:
            for i in range(len(q)): # take a snapshot of the length of the q
                r, c = q.popleft()
                
                # view current r, c as [0, 0]
                neighbors = [[1, 0], [-1, 0], [0, 1], [0, -1]] # this is bascially directions
                for dr, dc in neighbors:
                    if (r + dr < 0 or c + dc < 0 or 
                        r + dr == rows or c + dc == cols or
                        grid[r + dr][c + dc] != 1):
                        continue
                    grid[r + dr][c + dc] = 2
                    q.append((r + dr, c + dc))
                    fresh -= 1
            time += 1
        
        return -1 if fresh != 0 else time
```

## 286. Walls and Gates[[Link](https://leetcode.com/problems/walls-and-gates/description/)]

- video explaination[[Link](https://neetcode.io/problems/islands-and-treasure?list=neetcode250)]

```python
# time: O(m * n); space: O(m * n)
class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        rows, cols = len(rooms), len(rooms[0])
        visited = set()
        q = deque()

        def add_room(r, c):
            if (r < 0 or c < 0 or r == rows or c == cols 
                or (r, c) in visited or rooms[r][c] == -1):
                return
            visited.add((r, c))
            q.append((r, c))

        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:
                    q.append((r, c))
                    visited.add((r, c))
        
        distance = 0
        while q:
            for _ in range(len(q)):
                r, c = q.popleft()
                rooms[r][c] = distance
                add_room(r + 1, c)
                add_room(r - 1, c)
                add_room(r, c + 1)
                add_room(r, c - 1)
            distance += 1
```

## 417. Pacific Atlantic Water Flow[[Link](https://leetcode.com/problems/pacific-atlantic-water-flow/description/)]

- video explaination[[Link](https://neetcode.io/problems/pacific-atlantic-water-flow?list=neetcode250)]

```python
# time: O(m * n); space: O(m * n)
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        rows, cols = len(heights), len(heights[0])  # Dimensions of the grid
        pacific, atlantic = set(), set()  # Cells reachable by each ocean

        def dfs(r, c, visited, prev_height):
            """
            Reverse DFS: starting from the ocean, go inland to all cells 
            that are the same height or higher than the current cell.
            visited: set to track cells already processed for a given ocean
            prev_height: height of the cell we came from
            """
            if (r < 0 or c < 0 or r == rows or c == cols  # Out of bounds
                or (r, c) in visited                      # Already visited
                or heights[r][c] < prev_height):          # Can't flow uphill
                return 
            
            visited.add((r, c))  # Mark cell as reachable
            # Explore all four directions
            dfs(r + 1, c, visited, heights[r][c])
            dfs(r - 1, c, visited, heights[r][c])
            dfs(r, c + 1, visited, heights[r][c])
            dfs(r, c - 1, visited, heights[r][c])
        
        # Start DFS from the Pacific's edges (top row + left col)
        for c in range(cols):
            dfs(0, c, pacific, heights[0][c])             # Top row
            dfs(rows - 1, c, atlantic, heights[rows - 1][c]) # Bottom row
        
        for r in range(rows):
            dfs(r, 0, pacific, heights[r][0])              # Left column
            dfs(r, cols - 1, atlantic, heights[r][cols - 1]) # Right column
        
        # Intersection: cells reachable by both oceans
        res = []
        for r in range(rows):
            for c in range(cols):
                # so this postiion appear in both lookup table, then append to result
                if (r, c) in pacific and (r, c) in atlantic:
                    res.append([r, c])
        
        return res
"""
What is the Brute Force Approach?
Brute Force Idea:
For each cell in the grid:
    Run a DFS/BFS to check if it can reach the Pacific.
    Run another DFS/BFS to check if it can reach the Atlantic.
    If both are true, add it to the result. 
Why it’s bad:
    Each DFS can take O(m * n) time in the worst case.
    Doing it for every cell means O((m * n) * (m * n)) = O(m² * n²) complexity.

Key Idea: 
Instead of simulating water flow from every cell, you reverse the problem —
    Start from the oceans and work inwards, marking all cells that can reach that ocean.
    One starting from the Pacific’s borders.
    One starting from the Atlantic’s borders.
    In the end, the intersection of reachable cells from both traversals is your answer.

Time complexity:
    Each cell is visited at most once per ocean → O(m * n) total.
    Space complexity:
    Two visited sets → O(m * n) space.
"""
```