## 283. Move Zeroes[[Link](https://leetcode.com/problems/move-zeroes/description/?envType=study-plan-v2&envId=leetcode-75)]

- video explaination[[Link](https://neetcode.io/problems/move-zeroes?list=allNC)]

```python
# time: O(n); space: O(1)
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums) # range still need to scan
        l = 0
        
        while l < n:
            if nums[l] == 0:
                nums.append(nums[l])
                del nums[l]
                n -= 1
            else:
                l += 1
```

## 1679. Max Number of K-Sum Pairs[[Link](https://leetcode.com/problems/max-number-of-k-sum-pairs/description/?envType=study-plan-v2&envId=leetcode-75)]

```python
# time: O(n log n); space: O(1)
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        nums.sort()
        l, r = 0, len(nums) -1
        res = 0

        while l < r:
            val = nums[l] + nums[r]
            if val < k:
                l += 1
            elif val > k:
                r -= 1
            else:
                l += 1
                r -= 1
                res += 1
        return res
```

## 2239. Find Closest Number to Zero[[Link](https://leetcode.com/problems/find-closest-number-to-zero/description/)]

```python
class Solution:
    def findClosestNumber(self, nums: List[int]) -> int:
        res = []
        min_dist = float('inf')
        for n in nums:
            dist = abs(n - 0)
            if dist < min_dist:
                min_dist = dist
                res = [n] # reset list with new closest number
            elif dist == min_dist:
                res.append(n)
        
        return max(res)
```

## No.1
```python
def solution(commands):
    position = 0
    for c in commands:
        if c == "U":
            position += 1
        if c == "D":
            position -= 1

    if position > 0:
        return "U"
    if position < 0:
        return "D"
    return ""
```

## No.2
```python
def solution(departure_times, current_time):
    def to_minute(t):
        h, m = t.split(":")
        h, m = int(h), int(m)
        return h * 60 + m
    
    curr = to_minutes(curr_time)
    last_departure = -1

    for t in departure_times:
        tm = to_minute(t)
        if tm < curr:
            last_departure = tm
        else:
            break
    
    return -1 if last_departure == -1 else curr - last_departures
```

## No.3
```python
def solution(n: int, m: int, figures: list[str]) -> list[list[int]]:
    grid = [[0] * m for _ in range(n)]

    shapes = {
        'A': [[1]],
        'B': [[1, 1, 1]],
        'C': [[1, 1],
              [1, 1]],
        'D': [[1, 0],
              [1, 1],
              [1, 0]],
        'E': [[0, 1, 0],
              [1, 1, 1]],
    }

    def can_place(r, c, s):
        h, w = len(s), len(s[0])
        if r + h > n or c + w > m:
            return False
        # verify if 
        for i in range(h):
            for j in range(w):
                if s[i][j] and grid[r + i][c + j]:
                    return False
        return True
    
    def place(r, c, s, val):
        h, w = len(s), len(s[0])
        for i in range(h):
            for j in range(w):
                if s[i][j]:
                    grid[r + i][c + j] = val

    for i, figure in enumerate(figures):
        s = shapes[f]
        placed = False
        
        for r in range(n):
            if placed:
                break
            for c in range(m):
                if can_placed(r, c, s):
                    place(r, c, s, i + 1)
                    placed = True
                    break
    return grid
```

## No.4
```python
from collections import defaultdict

def solution(travelPhotos):
    adj_list = defaultdict(list)

    for u, v in travelPhotos:
        adj_list[u].append(v)
        adj_list[v].append(u)

    start = None
    for node, neighbors in adj_list.items():
        if len(neighbors) == 1:
            start = node
            break
    
    res = []
    visited = set()
    def dfs(node):
        visited.add(node)
        res.append(node)
        for nei in adj_list[node]:
            dfs(nei)
    
    dfs(start)
    return res
```

## No.5
```python
def solution(n):
    res = []
    for i in range(1, n + 1):
        s = ""
        if i == 1 or i == n:
            s = "*" * n
        else:
            space = " " * (n - 2)
            s = "*" + space + "*"
        res.append(s)
    return res
```

## No.6
