# Graph in LC

## 200. Number of Islands[[Link](https://leetcode.com/problems/number-of-islands/description/?envType=study-plan-v2&envId=top-interview-150)]
- __Concepts:__
    - An __island__ is a connected component of "1" cells, meaning a group of "1"s that are connected through their neighbors (up, down, left, or right). 
    - A "1" that is completely isolated (i.e., has only "0" neighbors) is still an island.

- video explaination[[Link](https://neetcode.io/problems/count-number-of-islands)]

```python
# in DFS
from typing import List

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0

        islands = 0
        rows, cols = len(grid), len(grid[0])
        visited = set()

        def dfs(r, c):
            # DFS to mark all connected '1's as visited
            if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == '0' or (r, c) in visited:
                return
            # grid[r][c] = '0' -> use this can also functioned as 'visited'
            visited.add((r, c))
            # explore 4 direction
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        
        # Iterate through the grid
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1' and (r, c) not in visited:
                    islands += 1
                    dfs(r, c)

        return islands

# or
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        visited = set() 

        def dfs(r, c):
            if (r < 0 or c < 0 or r == rows or c == cols or
                (r, c) in visited or grid[r][c] == '0'):
                return
            
            visited.add((r, c))
            dfs(r + 1, c) 
            dfs(r - 1, c)  
            dfs(r, c + 1)  
            dfs(r, c - 1)

        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1' and (r, c) not in visited:
                    dfs(r, c)
                    count += 1
        return count
```

## 695. Max Area of Island[[Link](https://leetcode.com/problems/max-area-of-island/description/)]

- video explaination[[Link](https://neetcode.io/problems/max-area-of-island)]

```python
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        visited = set()  

        def dfs(r, c):
            if (r < 0 or c < 0 or r == rows or c == cols or
                (r, c) in visited or grid[r][c] == 0):
                return 0 # this cover all base case, also include if all grid zero, return 0
            
            visited.add((r, c))
            count = 1 # so we can set count = 1 with no problem
            count += dfs(r + 1, c)
            count += dfs(r - 1, c)
            count += dfs(r, c + 1)
            count += dfs(r, c - 1)
            return count

        max_count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1 and (r, c) not in visited:
                    count = dfs(r, c)
                    max_count = max(max_count, count)
        
        return max_count
```

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

## 133. Clone Graph[[Link](https://leetcode.com/problems/clone-graph/description/?envType=study-plan-v2&envId=top-interview-150)]

__Answer__
- Explaination[[Link](https://neetcode.io/problems/clone-graph)]

```python
# DFS
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""
from typing import Optional
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None
        old_to_new = {}

        def dfs(node):
            if node in old_to_new:
                return old_to_new[node]
            
            # clone -> new node for clone graph
            clone = Node(node.val)
            old_to_new[node] = clone
            # recursively clone the neigbhor
            for neighbor in node.neighbors:
                clone.neighbors.append(dfs(neighbor))
            return clone
        
        return dfs(node)
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

## 207. Course Schedule[[Link](https://leetcode.com/problems/course-schedule/description/?envType=study-plan-v2&envId=top-interview-150)]

- Video Explaination[[Link](https://www.youtube.com/watch?v=EgI5nU9etnU)]
- hint: construct the adjacency list and evalutate if meet requirements(detect cycle or not)
```python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        pre_map_adjlist = {i:[] for i in range(numCourses)}
        # feed adj List
        for crs, pre in prerequisites:
            pre_map_adjlist[crs].append(pre)

        # visited set
        visited = set() 
        def dfs(crs):
            if crs in visited:
                return False
            
            if pre_map_adjlist[crs] == []:
                return True
            
            visited.add(crs)
            # looking through the neighbor
            for pre in pre_map_adjlist[crs]:
                if not dfs(pre):
                    return False
            visited.remove(crs)
            pre_map_adjlist[crs] = [] # add this line to reduce time executed
            return True
        # need to manually loop to cover the disconnected graph cases
        for crs in range(numCourses):
            if not dfs(crs):
                return False
        
        return True
            
```
- Time Complexity: O(N + P)

## 210. Course Schedule II[[Link](https://leetcode.com/problems/course-schedule-ii/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://www.youtube.com/watch?v=Akt3glAwyfY&t=578s)]

```python
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # build adjacency list for prereqs
        prereq = {c:[] for c in range(numCourses)}
        for crs, pre in prerequisites:
            prereq[crs].append(pre)

        # a course has 3 possible states:
        # visited -> crs has been added to output
        # visiting -> crs not added to output, but added to cycle
        # unvisited -> crs not added to output or cycle
        output = []
        visited, cycle = set(), set()

        def dfs(crs):
            if crs in cycle:
                return False
            if crs in visited:
                return True
            
            cycle.add(crs)
            for pre in prereq[crs]:
                if not dfs(pre):
                    return False
            cycle.remove(crs)
            visited.add(crs)
            output.append(crs)
            return True
        
        for c in range(numCourses):
            if not dfs(c):
                return []
        return output
```
- Time Complexity: O(E + V) / O(N + P)

## 909. Snakes and Ladders[[Link](https://leetcode.com/problems/snakes-and-ladders/?envType=study-plan-v2&envId=top-interview-150)]

- Vide Explaination[[Link](https://www.youtube.com/watch?v=6lH4nO3JfLk)]
```python
# BFS in graph
class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        length = len(board)
        board.reverse()

        def int_to_pos(square): # -> get position
            r = (square - 1) // length
            c = (square - 1) % length
            if r % 2:
                c = length - 1 - c
            return r, c

        q = deque() # [square, moves] moves -> number of moves to get this square from start
        q.append([1, 0])
        visit = set()

        while q:
            square, moves = q.popleft()
            for i in range(1, 7):
                next_square = square + i
                r, c = int_to_pos(next_square)

                if board[r][c] != -1:
                    next_square = board[r][c]
                if next_square == length * length: # reached last square
                    return moves + 1 # -> moves is the number of moves to get "this" square
                if next_square not in visit:
                    visit.add(next_square)
                    q.append([next_square, moves + 1])
        return -1
```

## 433. Minimum Genetic Mutation[[Link](https://leetcode.com/problems/minimum-genetic-mutation/description/?envType=study-plan-v2&envId=top-interview-150)]

- Video Expalination[[Link](https://www.youtube.com/watch?v=9lkn3rHCSLg)]
```python
class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        q = deque()
        q.append([startGene, 0])
        visited = set()
        visited.add(startGene)

        while q:
            curr_gene, weight = q.popleft()
            if curr_gene == endGene:
                return weight
            
            for c in 'ACGT':
                for i in range(len(curr_gene)):
                    neighbor = curr_gene[:i] + c + curr_gene[i + 1:]
                    if neighbor not in visited and neighbor in bank:
                        q.append([neighbor, weight + 1])
                        visited.add(neighbor)

        return -1
```

## 127. Word Ladder[[Link](https://leetcode.com/problems/word-ladder/?envType=study-plan-v2&envId=top-interview-150)]

- Vide Explaination[[Link](https://www.youtube.com/watch?v=h9iTnkgv05E)]

```python
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # construct adjacency list from word list
        if endWord not in wordList:
            return 0
        
        nei = collections.defaultdict(list)
        wordList.append(beginWord)
        for word in wordList:
            for j in range(len(word)):
                pattern = word[:j] + "*" + word[j + 1:]
                nei[pattern].append(word)
        
        visited = set()
        visited.add(beginWord)
        q = deque()
        q.append(beginWord)
        res = 1
        while q:
            for i in range(len(q)):
                word = q.popleft()
                if word == endWord:
                    return res
                for j in range(len(word)):
                    pattern = word[:j] + "*" + word[j + 1:]
                    for neiWord in nei[pattern]:
                        if neiWord not in visited:
                            visited.add(neiWord)
                            q.append(neiWord)

            res += 1
        return 0
```