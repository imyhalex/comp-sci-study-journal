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

## 133. Clone Graph[[Link](https://leetcode.com/problems/clone-graph/description/?envType=study-plan-v2&envId=top-interview-150)]

__Answer__
- Explaination[[Link](https://neetcode.io/problems/clone-graph)]
- hint: the visited in this question should be a hashmap that map old node to new clone node: old_to_new = 
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

## 207. Course Schedule[[Link](https://leetcode.com/problems/course-schedule/description/?envType=study-plan-v2&envId=top-interview-150)]

- Video Explaination[[Link](https://www.youtube.com/watch?v=EgI5nU9etnU)]
- hint: construct the adjacency list and evalutate if meet requirements(detect cycle or not)
```python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adj_list = defaultdict(list)
        for crs, pre in prerequisites:
            adj_list[crs].append(pre)
        
        path = set()
        visited = set()
        def dfs(crs):
            if crs in path:
                return False
            if crs in visited:
                return True
            
            path.add(crs)
            for pre in adj_list[crs]:
                if not dfs(pre):
                    return False
            path.remove(crs)
            visited.add(crs)
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

## 630. Course Schedule III[[Link](https://leetcode.com/problems/course-schedule-iii/description/)]
- Greedy + Max Heap Intuition:
    - Sort courses by lastDay so you consider the most urgent ones first.
    - Maintain a running total of time spent.
    - Use a max-heap to keep track of the durations of the courses you've taken.
    - If adding a course causes you to go over its lastDay, remove the longest course you've taken (since it cost the most time).
```python
# time & space: O(n log n)
class Solution:
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        # sort courses by their deadlines
        courses.sort(key=lambda x: x[1])

        current_total_time = 0
        max_heap = []

        for duration, last_day in courses:
            current_total_time += duration
            heapq.heappush(max_heap, -duration) # max-heap pushing negative value

            if current_total_time > last_day:
                # drop the longest duration course to fit the deadline
                current_total_time += heapq.heappop(max_heap) # remove the largest duration (since in python, the max_heap is represents numbers in negative, just add it)
        
        return len(max_heap)
```

## *1462. Course Schedule IV[[Link](https://leetcode.com/problems/course-schedule-iv/description/)]
- video explaination[[Link](https://neetcode.io/problems/course-schedule-iv?list=neetcode150)]

```python
# time: O(V * (V + E) + m); space: O(V^2 + E + m)
class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        adj_list = defaultdict(list)
        for pre, crs in prerequisites:  # original edge pre → crs
            adj_list[crs].append(pre) # store it as crs → pre
        
        prereq_map = {}
        def dfs(crs):
            if crs not in prereq_map:  # first time we see this course
                prereq_map[crs] = set()
                for pre in adj_list[crs]: # walk *backwards* to every prerequisite
                    prereq_map[crs] |= dfs(pre)  # union with their prerequisite sets
                prereq_map[crs].add(crs) # add itself (handy for queries) (optional)
            return prereq_map[crs]
        """
        why return prereq_map[crs]?
            - dfs(crs) is solving for one specific course
            - It's computing: "What are the prerequisites of course crs?"
            - So it only needs to return the result for that course: prereq_map[crs]
            
            for pre in adj_list[crs]:
                prereq_map[crs] |= dfs(pre)
            Here: You're saying: "Get the prerequisites of course pre (a prerequisite of crs) using dfs(pre)"
                The return value should be: "just the set of prerequisites for pre" — which is prereq_map[pre]
                So dfs(pre) returns prereq_map[pre]
        """
        # iterate throughh every single course (start from every single course) and construct the map
        for crs in range(numCourses):
            dfs(crs)

        res = []
        for u, v in queries:
            res.append(u in prereq_map[v])
        return res
```

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

## 743. Network Delay Time[[Link](https://leetcode.com/problems/network-delay-time/description/)]
- video explaination[[Link](https://neetcode.io/problems/network-delay-time?list=neetcode150)]

```python
# time: O(E log V); space: O(v + E)
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        adj_list = defaultdict(list)
        for u, v, w in times:
            adj_list[u].append((v, w))
        
        min_heap = [(0, k)]
        visited = set()
        t = 0 # for result
        while min_heap:
            w1, n1 = heapq.heappop(min_heap)
            if n1 in visited:
                continue
            visited.add(n1)
            t = max(t, w1)

            for n2, w2 in adj_list[n1]:
                if n2 not in visited:
                    heapq.heappush(min_heap, (w1 + w2, n2))
        
        return t if len(visited) == n else -1
```

## 1514. Path with Maximum Probability[[Link](https://leetcode.com/problems/path-with-maximum-probability/description/)]

- video explaination[[Link](https://neetcode.io/solutions/path-with-maximum-probability)

```python
# time: O(V + E log V); space: O(V + E)
class Solution:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start_node: int, end_node: int) -> float:
        adj_list = defaultdict(list)
        for i in range(len(edges)):
            src, dst = edges[i]
            adj_list[src].append((dst, succProb[i]))
            adj_list[dst].append((src, succProb[i]))
        
        max_heap = [(-1, start_node)]
        visited = set()

        while max_heap:
            p1, n1 = heapq.heappop(max_heap)
            visited.add(n1)
            if n1 == end_node:
                return -p1
            
            for n2, p2 in adj_list[n1]:
                if n2 not in visited:
                    heapq.heappush(max_heap, (p2 * p1, n2))
        
        return 0
```

## 778. Swim in Rising Water[[Link](https://leetcode.com/problems/swim-in-rising-water/description/)]

- video explaination[[Link](https://neetcode.io/problems/swim-in-rising-water?list=neetcode150)]

```python
# time: O(n ^ 2 log n); space: O(n ^ 2)
class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        visited = set()
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]] 
        min_heap = [(grid[0][0], 0, 0)] # (time or max-length, r, c)
        
        visited.add((0, 0))
        while min_heap:
            t, r, c = heapq.heappop(min_heap)

            if r == n - 1 and c == n - 1:
                return t
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (nr < 0 or nc < 0 or nr == n or nc == n or
                    (nr, nc) in visited):
                    continue
                visited.add((nr, nc))
                heapq.heappush(min_heap, (max(t, grid[nr][nc]), nr, nc))
```

## 1631. Path With Minimum Effort[[Link](https://leetcode.com/problems/path-with-minimum-effort/description/)]

- video explaination[[Link](https://neetcode.io/problems/path-with-minimum-effort?list=neetcode250)]

```python
# time: O(m * n * log(m * n)); sapce:O(m * n)
class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        rows, cols = len(heights), len(heights[0])
        visited = set()
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        min_heap = [(0, 0, 0)] # (effort, r, c)

        while min_heap:
            e, r, c = heapq.heappop(min_heap)

            if (r, c) in visited:
                continue
            
            visited.add((r, c))

            if r == rows - 1 and c == cols - 1:
                return e
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (nr < 0 or nc < 0 or nr == rows 
                    or nc == cols or (nr, nc) in visited):
                    continue
                next_effort = abs(heights[nr][nc] - heights[r][c])
                heapq.heappush(min_heap, (max(e, next_effort), nr, nc))
        return 0
```

## 1584. Min Cost to Connect All Points[[Link](https://leetcode.com/problems/min-cost-to-connect-all-points/description/)]

- video explaination[[Link](https://neetcode.io/problems/min-cost-to-connect-points?list=neetcode150)]

```python
# Example 2:

# Input: points = [[3,12],[-2,5],[-4,1]]
# Output: 18

# adj = {
#     0: [[dist(0,1), 1], [dist(0,2), 2]],
#     1: [[dist(1,0), 0], [dist(1,2), 2]],
#     2: [[dist(2,0), 0], [dist(2,1), 1]]
# }

# time: O(n^2 log n); space: O(n^2)
class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        adj_list = {i:[] for i in range(n)} # adj_list node_index -> [(distance(or weight, node_index))]

        for i in range(n):
            x1, y1 = points[i]
            for j in range(i + 1, n):
                x2, y2 = points[j]
                dist = abs(x1 - x2) + abs(y1 - y2)
                adj_list[i].append((dist, j))
                adj_list[j].append((dist, i))
        
        res = 0
        visited = set()
        min_heap = [(0, 0)] # (cost, node_index)
        while min_heap:
            cost, i = heapq.heappop(min_heap)
            if i in visited:
                continue
            res += cost
            visited.add(i)
            for nei_cost, nei_idx in adj_list[i]:
                if nei_idx not in visited:
                    heapq.heappush(min_heap, (nei_cost, nei_idx))
        
        return res

```

## **1489. Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree[[Link](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/description/)]

- video explaination[[Link](https://neetcode.io/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree?list=neetcode150)]

```python
# time: O(E^2); space: O(V + E)
class UnionFind:
    def __init__(self, n):
        self.par = [i for i in range(n)]
        self.rank = [1] * n

    def find(self, v1):
        while v1 != self.par[v1]:
            self.par[v1] = self.par[self.par[v1]]
            v1 = self.par[v1]
        return v1

    def union(self, v1, v2):
        p1, p2 = self.find(v1), self.find(v2)
        if p1 == p2:
            return False
        if self.rank[p1] > self.rank[p2]:
            self.par[p2] = p1
            self.rank[p1] += self.rank[p2]
        else:
            self.par[p1] = p2
            self.rank[p2] += self.rank[p1]
        return True


class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        for i, e in enumerate(edges):
            e.append(i)  # [v1, v2, weight, original_index]

        edges.sort(key=lambda e: e[2])

        mst_weight = 0
        uf = UnionFind(n)
        for v1, v2, w, i in edges:
            if uf.union(v1, v2):
                mst_weight += w

        critical, pseudo = [], []
        for n1, n2, e_weight, i in edges:
            # Try without curr edge
            weight = 0
            uf = UnionFind(n)
            for v1, v2, w, j in edges:
                if i != j and uf.union(v1, v2):
                    weight += w
            if max(uf.rank) != n or weight > mst_weight:
                critical.append(i)
                continue

            # Try with curr edge
            uf = UnionFind(n)
            uf.union(n1, n2)
            weight = e_weight
            for v1, v2, w, j in edges:
                if uf.union(v1, v2):
                    weight += w
            if weight == mst_weight:
                pseudo.append(i)
        return [critical, pseudo]
```