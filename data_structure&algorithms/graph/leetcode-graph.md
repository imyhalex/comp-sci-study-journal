# Graph in LC

## 200. Number of Islands[[Link](https://leetcode.com/problems/number-of-islands/description/?envType=study-plan-v2&envId=top-interview-150)]

```text
Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are 
all surrounded by water.
 
Example 1:
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1

Example 2:
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]

Explianition:
1  1  0  0  0
1  1  0  0  0
0  0  1  0  0
0  0  0  1  1

Now, let's identify the islands:

Island #1 (Top-left corner):
    The "1"s at positions (0,0), (0,1), (1,0), (1,1) are all connected.
    These form one island.  
    Island #2 (Middle of the grid):

The "1" at (2,2) is isolated, meaning it has no adjacent "1" neighbors.
    This forms a second island.
    Island #3 (Bottom-right corner):

The "1"s at (3,3), (3,4) are connected.
    These form a third island.

Output: 3
```

- __Concepts:__
    - An __island__ is a connected component of "1" cells, meaning a group of "1"s that are connected through their neighbors (up, down, left, or right). 
    - A "1" that is completely isolated (i.e., has only "0" neighbors) is still an island.



__Answer__
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
```
- Explaination[[Link](https://www.youtube.com/watch?v=HpinqiqiXUQ)]
```python
# BFS
from typing import List
from collections import deque

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        
        islands = 0
        visited = set()
        rows, cols = len(grid), len(grid[0])

        def bfs(r, c):
            q = deque()
            visited.add((r, c))
            q.append((r, c))

            while q:
                row, col = q.popleft()
                directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

                for dr, dc in directions:
                    r, c = row + dr, col + dc
                    if 0 <= r < rows and 0 <= c < cols and grid[r][c] == '1' and (r, c) not in visited:
                        q.append((r, c))
                        visited.add((r, c))

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1' and (r, c) not in visited:
                    islands += 1
                    bfs(r, c)
        
        return islands
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

```text
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

For simplicity, each node's value is the same as the node's index (1-indexed). For example, the first node with val == 1, the second node with val == 2, and so on. The graph is represented in the test case using an adjacency list.

An adjacency list is a collection of unordered lists used to represent a finite graph. Each list describes the set of neighbors of a node in the graph.

The given node will always be the first node with val = 1. You must return the copy of the given node as a reference to the cloned graph.

Example 1:

Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
Output: [[2,4],[1,3],[2,4],[1,3]]
Explanation: There are 4 nodes in the graph.
1st node (val = 1)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
2nd node (val = 2)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
3rd node (val = 3)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
4th node (val = 4)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).

Example 2:
Input: adjList = [[]]
Output: [[]]
Explanation: Note that the input contains one empty list. The graph consists of only one node with val = 1 and it does not have any neighbors.
Example 3:

Input: adjList = []
Output: []
Explanation: This an empty graph, it does not have any nodes.
```

__Answer__
- Explaination[[Link](https://www.youtube.com/watch?v=mQeF6bN8hMk)]

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
        
        # a dictionary to map a original nodes to colned node
        visited = {}

        def dfs(start):
            if start in visited:
                return visited[start]
            
            # clone -> new start node for clone graph
            clone = Node(start.val)
            visited[start] = clone

            # recursively clone the neigbhor
            for neighbor in start.neighbors:
                clone.neighbors.append(dfs(neighbor))

            return clone

        return dfs(node)
```