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