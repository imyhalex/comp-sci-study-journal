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

## 752. Open the Lock[[Link](https://leetcode.com/problems/open-the-lock/description/)]

- video explaination[[Link](https://neetcode.io/problems/open-the-lock?list=neetcode250)]

```python
# time: O(d ^ n + m); space: O(d ^ n)
class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        q = deque()
        q.append(("0000", 0)) # [lock, num of turns]
        visited = set()
        deadends = set(deadends)

        if "0000" in deadends:
            return -1
        
        # helper function: doing actual spin for the 4-circular wheels lock
        def children(lock):
            res = []
            for i in range(4):
                digit = str((int(lock[i]) + 1) % 10)
                res.append(lock[:i] + digit + lock[i+1:])
                digit = str((int(lock[i]) - 1 + 10) % 10)
                res.append(lock[:i] + digit + lock[i+1:])
            return res

        while q:
            lock, turns = q.popleft()
            if lock == target:
                return turns
            for child in children(lock):
                if child not in visited and child not in deadends:
                    visited.add(child)
                    q.append((child, turns + 1))
        return -1

```

## 463. Island Perimeter[[Link](https://leetcode.com/problems/island-perimeter/description/)]

- video explaination[[Link](https://neetcode.io/problems/island-perimeter?list=neetcode250)]

```python
# time: O(m * n); space: o(m * n)
class Solution:
    def islandPerimeter(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        visited = set()

        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == 0:
                return 1
            
            if (r, c) in visited:
                return 0
            
            visited.add((r, c))
            perimeter = dfs(r + 1, c)
            perimeter += dfs(r - 1, c)
            perimeter += dfs(r, c + 1)
            perimeter += dfs(r, c - 1)

            return perimeter
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != 0:
                    return dfs(r, c)
```

## 953. Verifying an Alien Dictionary[[Link](https://leetcode.com/problems/verifying-an-alien-dictionary/description/)]

- video explaination[[Link](https://neetcode.io/problems/verifying-an-alien-dictionary?list=neetcode250)]

```python
# time: O(n * m log n); space: O(n * m)
class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        order_index = {c: i for i, c in enumerate(order)}

        def compare(word):
            return [order_index[c] for c in word]
        
        return words == sorted(words, key=compare)

# time: O(n * m); space: O(1) since 26 different characters
class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        order_index = {c: i for i, c in enumerate(order)}

        """
        w1 = "app"
        w2 = "apple"

        list(zip(w1, w2)) → [('a', 'a'), ('p', 'p'), ('p', 'p')]
        """
        def compare(w1, w2):
            for c1, c2 in zip(w1, w2):
                if order_index[c1] < order_index[c2]:
                    return True
                if order_index[c1] > order_index[c2]:
                    return False
            # if all characters matched; now shorter word should come first
            return len(w1) <= len(w2)
        
        for i in range(len(words) - 1):
            if not compare(words[i], words[i + 1]):
                return False
        
        return True
```

## 130. Surrounded Regions[[Link](https://leetcode.com/problems/surrounded-regions/description/?envType=study-plan-v2&envId=top-interview-150)]

```text
You are given an m x n matrix board containing letters 'X' and 'O', capture regions that are surrounded:

- Connect: A cell is connected to adjacent cells horizontally or vertically.
- Region: To form a region connect every 'O' cell.
- Surround: The region is surrounded with 'X' cells if you can connect the region with 'X' cells and none of the region cells are on the edge of the board.
- To capture a surrounded region, replace all 'O's with 'X's in-place within the original board. You do not need to return anything.

Example 1:

Input: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]

Output: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]

```
__Hints to solve this problem__
```text
Approach:
Identify the 'O' regions that should not be flipped:

Any 'O' cell that is connected to the border must remain 'O'.
We will use DFS or BFS to mark all 'O' cells connected to the border.
Change all the unmarked 'O's to 'X':

If an 'O' is not connected to the border, it must be surrounded, so we flip it to 'X'.
Restore the temporarily marked 'O's back to 'O':

Border-connected 'O's were temporarily marked (e.g., as 'T'), so we change them back to 'O'.
```

__Answer__
```python
# time: O(m * n); space: O(m * n)
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        if not board or not board[0]:
            return
        
        rows, cols = len(board), len(board[0])

        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != 'O':
                return
            board[r][c] = 'T'  # Temporarily mark as safe -> same functionality as visited
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        # caputer the surrounded region
        # statement: capture everything except unsurrounded region
        # Step 1: Mark all 'O's connected to the border as visited
        for r in range(rows):
            for c in [0, cols - 1]:
                if board[r][c] == 'O':
                    dfs(r, c)
        for c in range(cols):
            for r in [0, rows - 1]:
                if board[r][c] == 'O':
                    dfs(r, c)

        # Step 2: Convert all remaining 'O's to 'X' and keep visited as 'O'
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'
                elif board[r][c] == 'T':
                    board[r][c] = 'O'
```

## 261. Graph Valid Tree[[Link](https://leetcode.com/problems/graph-valid-tree/description/)]

- video explaination[[Link](https://neetcode.io/problems/valid-tree?list=neetcode250)]

```python
# time: O(V + E); space: O(V + E)
class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1: # two fews or too many
            return False

        adj = {i:[] for i in range(n)}
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        
        visited = set() # how many nodes are connect
        def dfs(node, parent):
            if node in visited:
                return False
            
            visited.add(node):
            for nei in adj[node]:
                if node == parent:
                    continue
                if not dfs(nei, node):
                    return False
            
            return True
        
        # finally, if len(visited) == number of node, then they are all connected, which means is valid tree
        # set par for head -1
        return dfs(0, -1) and n == len(visited)
```

## 399. Evaluate Division[[Link](https://leetcode.com/problems/evaluate-division/description/?envType=study-plan-v2&envId=top-interview-150)]

- Vide Explaination[[Link](https://www.youtube.com/watch?v=Uei1fwDoyKk)]

```python
class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        adj = collections.defaultdict(list) # Map a -> list of [b, a/b]
        for i, eq in enumerate(equations):
            a, b = eq
            adj[a].append([b, values[i]])
            adj[b].append([a, 1 / values[i]])
        
        def bfs(src, target):
            if src not in adj or target not in adj:
                return -1
            q, visit = deque(), set()
            q.append([src, 1])
            visit.add(src)
            while q:
                n, w = q.popleft()
                if n == target:
                    return w
                for nei, weight in adj[n]:
                    if nei not in visit:
                        q.append([nei, w * weight])
                        visit.add(nei)
            return - 1

        return [bfs(q[0], q[1]) for q in queries]
```

## 733. Flood Fill[[Link](https://leetcode.com/problems/flood-fill/description/)]

- video explaination[[Link](https://neetcode.io/problems/flood-fill?list=allNC)]

```python
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        rows, cols = len(image), len(image[0])
        start = image[sr][sc]
        visited = set()
        def dfs(r, c):
            if (r < 0 or c < 0 or r == rows or c == cols
                or (r, c) in visited or image[r][c] != start):
                return
            image[r][c] = color
            visited.add((r, c))
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        
        dfs(sr, sc)
        return image
```

## 1267. Count Servers that Communicate[[Link](https://leetcode.com/problems/count-servers-that-communicate/description/)]

- video explaination[[Link](https://neetcode.io/solutions/count-servers-that-communicate)]

```python
# time: O(n * m)
class Solution:
    def countServers(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        # precalcuation of number of servers in rows & cols
        row_count = [0] * rows # row -> count
        col_count = [0] * cols # col -> count
        res = 0

        # first pass: count servers in each row and column
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    row_count[r] += 1
                    col_count[c] += 1
        
        # second pass: count servers that can communicate
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] and (row_count[r] > 1 or col_count[c] > 1):
                    res += 1

        return res

"""
Leetcode 1572. Matrix Diagonal Sum

Leetcode 566. Reshape the Matrix

Leetcode 54. Spiral Matrix (counting grid positions)

Leetcode 1582. Special Positions in a Binary Matrix
"""
```


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

## 2924. Find Champion II[[Link](https://leetcode.com/problems/find-champion-ii/description/)]

- video explaination[[Link](https://neetcode.io/solutions/find-champion-ii)]

```python
# time: O(n + E); space: O(n)
class Solution:
    def findChampion(self, n: int, edges: List[List[int]]) -> int:
        # count the number of incomming edges
        incoming = [0] * n

        for src, dst in edges:
            incoming[dst] += 1
        
        champions = []
        for i, incoming_cnt in enumerate(incoming):
            if not incoming_cnt:
                champions.append(i)
        
        return -1 if len(champions) > 1 else champions[0]
```

## 2658. Maximum Number of Fish in a Grid[[Link](https://leetcode.com/problems/maximum-number-of-fish-in-a-grid/description/)]

- video explaination[[Link](https://neetcode.io/solutions/maximum-number-of-fish-in-a-grid)]

```python
# time & space: O(m * n)
class Solution:
    def findMaxFish(self, grid: List[List[int]]) -> int:
        """
        Approach:
        1. traverse all cells in a grid
        2. when find the cell is > 0 , do dfs to explore all the whole connected area
        3. sum all values within this component
        4. keep track of maximum fish count among all component
        """
        rows, cols = len(grid), len(grid[0])
        visited = set()

        def dfs(r, c):
            if (r < 0 or c < 0 or r == rows or c == cols
                or (r, c) in visited or grid[r][c] == 0):
                return 0
            
            visited.add((r, c))
            total = grid[r][c]
            total += dfs(r + 1, c)
            total += dfs(r - 1, c)
            total += dfs(r, c + 1)
            total += dfs(r, c - 1)

            return total
        
        max_fish = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] > 0 and (r, c) not in visited:
                    max_fish = max(max_fish, dfs(r, c))
        return max_fish
```

## 1905. Count Sub Islands[[Link](https://leetcode.com/problems/count-sub-islands/description/)]

- video explaination[[Link](https://neetcode.io/solutions/count-sub-islands)]

```python
# time: O(m * n); space: O(m * n)
class Solution:
    def countSubIslands(self, grid1: List[List[int]], grid2: List[List[int]]) -> int:
        rows, cols = len(grid1), len(grid1[0])
        visited = set()

        def dfs(r, c) -> bool:
            if (r < 0 or c < 0 or r == rows or c == cols
                or (r, c) in visited or grid2[r][c] == 0):
                return True

            visited.add((r, c))
            res = True
            if grid1[r][c] == 0: # case that definitly not a sub island
                res = False
            res = dfs(r + 1, c) and res
            res = dfs(r - 1, c) and res
            res = dfs(r, c + 1) and res
            res = dfs(r, c - 1) and res
            return res

        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid2[r][c] and (r, c) not in visited and dfs(r, c):
                    count += 1
        return count
```

## 1466. Reorder Routes to Make All Paths Lead to the City Zero[[Link](https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/description/)]

- video explaination[[Link](https://neetcode.io/solutions/reorder-routes-to-make-all-paths-lead-to-the-city-zero)]
```python
# time: O(n); space: O(n)
class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        """
        start af city 0, this means things such as even u->v 4->0 has flag = 1 does not get count
        becasue the starting point is city 0 so this is follows the v->u correct order with flag = 0
        recursively check its neigbors
        count outgoing edges
        """
        adj_list = defaultdict(list)
        visited = set()

        for u, v in connections:
            # only the shape in u -> v have possiblility to reverse, so we mark it as 1
            adj_list[u].append((v, 1)) # original edges u -> v
            adj_list[v].append((u, 0)) # reverse edge, does not need change
        
        """
        When we traverse from node 0, we’ll go to all neighbors.

        If the edge we traverse has a flag 1, it was originally u → v, which is away from 0 → needs to be reversed.

        If the flag is 0, it’s already pointing toward 0 → no change needed.
        """
        def dfs(node):
            visited.add(node)
            changes = 0
            for nei, needs_change in adj_list[node]:
                if nei not in visited:
                    changes += needs_change + dfs(nei)
            return changes
        
        return dfs(0)

```

## 909. Snakes and Ladders[[Link](https://leetcode.com/problems/snakes-and-ladders/description/)]

```py

```

## 802. Find Eventual Safe States[[Link](https://leetcode.com/problems/find-eventual-safe-states/description/)]

- video explaination[[Link](https://neetcode.io/solutions/find-eventual-safe-states)]

```py

```