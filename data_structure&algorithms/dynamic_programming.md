# Dynamic Programming

__What is dynamic programming?__
- Simply put, it is an optimized version of recursion.
- It takes a big problem and solves it by breaking it down into smaller problems. 
- he reason we say it is optimized recursion is because it is often more optimal when it comes to time and space.

## 1-Dimension DP[[Link](https://neetcode.io/courses/dsa-for-beginners/32)]

__Brute Force Approach(Withou no DP)__
```python
def bruteForce(n):
    if n <= 1:
        return n
    return bruteForce(n - 1) + bruteForce(n - 2)
```

### Top Down Approach(Memorization)
- Time Complexity get optimized to: O(n)
```python
def fib(n, cache):
    if n <= 1:
        return n

    if n in cache:
        return cache[n]
    
    cache[n] = fib(n - 1, cache) + fib(n - 2, cache)

    return cache[n]
```

### Bottom Up Approach(Tabulation)
- Time Complexity get optimized to: O(n)
```python
def fib(n):
    if n < 2:
        return n
    
    dp = [0, 1]
    i = 2
    while i <= n:
        tmp = dp[1]
        dp[1] = dp[0] + dp[1]
        dp[0] = tmp
        i += 1
    return dp[1]
```
## 2-Dimension DP[[Link](https://neetcode.io/courses/dsa-for-beginners/33)]

- Q: Count the number of unique paths from the top left to the bottom right in a 2d array. You are only allowed to move down or to the right.

__Brute Force(with no dp)__
```python
# Brute Force - Time: O(2 ^ (n + m)), Space: O(n + m)
def bruteForce(r, c, rows, cols):
    if r == rows or c == cols:
        return 0
    if r == rows - 1 and c == cols - 1:
        return 1
    
    return (bruteForce(r + 1, c, rows, cols) +  bruteForce(r, c + 1, rows, cols))
```

### Top-Down Approach(Memorization)
```python
# Memoization - Time and Space: O(n * m)
def memorization(r, c, rows, cols, cache):
    if r == rows or c == cols:
        return 0
    
    if cache[r][c] > 0:
        return cache[r][c]
    
    if r == row - 1 and c == cols - 1:
        return 1
    
    cache[r][c] = (memorization(r + 1, c, rows, cols, cache) + memorization(r, c + 1, rows, cols, cache))

    return cache[r][c]
```

### Bottom-UP Approach("True" Dynamic)
```python
# Dynamic Programming - Time: O(n * m), Space: O(m), where m is num of cols
def dp(rows, cols):
    # base case - strat at last plus one row
    prev_row = [0] * cols

    for r in range(rows - 1, -1, -1):
        curr_row = [0] * cols
        curr_row[cols - 1] = 1
        for c in range(cols - 2, -1, -1):
            curr_row[c] = curr_row[c + 1] + prev_row[c]
        prev_row = curr_row
    
    return prev_row[0]
```

## Some LC Problems

### 70. Climbing Stairs[[Link](https://leetcode.com/problems/climbing-stairs/description/)]
```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n < 2:
            return n
        
        dp = [1, 1]
        i = 2
        while i <= n:
            tmp = dp[1]
            dp[1] = dp[0] + dp[1]
            dp[0] = tmp
            i += 1
        
        return dp[1]
```

### 198. House Robber[[Link](https://leetcode.com/problems/house-robber/description/)]
```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0

        if len(nums) == 1:
            return nums[0]
    
        dp = [0, 0]
        for n in nums:
            tmp = max(dp[1], dp[0] + n)
            dp[0] = dp[1] # override
            dp[1] = tmp # make sure dp[1] have most up-to-date num

        return dp[1]
```

### 139. Word Break[[Link](https://leetcode.com/problems/word-break/description/?envType=study-plan-v2&envId=top-interview-150)]
<!-- ```python
# BFS
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        q = deque([0])
        seen = set()

        while q:
            start = q.popleft()
            if start == len(s):
                return True
            
            for end in range(start + 1, len(s) + 1):
                if end in seen:
                    continue
                
                if s[start:end] in words:
                    q.append(end)
                    seen.add(end)
        
        return False
``` -->

- Video Explaination[[Link](https://www.youtube.com/watch?v=Sx9NNgInc3A)]

```python
# Bottom Up Approach
# -Time Complexity: O(n⋅m⋅k); Space: O(n)
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        dp = [False] * (len(s) + 1)
        dp[len(s)] = True # base case: empty string "" for start

        for i in range(len(s) - 1, -1, -1):
            for w in wordDict:
                if (i + len(w)) <= len(s) and s[i: i + len(w)] == w:
                    dp[i] = dp[i + len(w)]

                if dp[i]:
                    break

        return dp[0]
```

### Unique Paths[[Link](https://neetcode.io/problems/count-paths)]
```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        prev = [0] * n

        for r in range(m - 1, -1, -1):
            curr = [0] * n
            curr[n - 1] = 1
            for c in range(n - 2, -1, -1):
                curr[c] = curr[c + 1] + prev[c]
            prev = curr
        
        return prev[0]
```

### 63. Unique Paths II[[Link](https://leetcode.com/problems/unique-paths-ii/description/?envType=study-plan-v2&envId=top-interview-150)]
```python
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        rows, cols = len(obstacleGrid), len(obstacleGrid[0])

        if obstacleGrid[rows - 1][cols - 1] == 1 or obstacleGrid[0][0]:
            return 0
            
        prev = [0] * cols
        for r in range(rows - 1, -1, -1):
            curr = [0] * cols
            if obstacleGrid[r][cols - 1] != 1:
                curr[cols - 1] = prev[cols - 1] if r < rows - 1 else 1
            
            for c in range(cols - 2, -1, -1):
                if obstacleGrid[r][c] != 1:
                    curr[c] = curr[c + 1] + prev[c]
            prev = curr
        
        return prev[0]
```

#### Why `curr[cols - 1] = prev[cols - 1] if r < rows - 1 else 1`

Inside the outer loop we’re visiting the grid **row‑by‑row from bottom to top**.  
For every row we fill the 1‑D DP array `curr` **from right to left**.

```python
# bottom‑most row gets its seed value
if obstacleGrid[r][cols‑1] != 1:
    curr[cols‑1] = prev[cols‑1] if r < rows‑1 else 1
```

| situation | what the line does | why it works |
|-----------|-------------------|--------------|
| **Bottom row (`r == rows‑1`)** | sets `curr[last] = 1` (if cell is open) | On the goal row the only way to reach the target from that cell is to keep moving right, so there is exactly **one** way if the cell itself isn’t an obstacle. |
| **Any higher row (`r < rows‑1`)** | copies `prev[last]`, i.e. the value computed for the row **directly beneath** | Moving in the last column you can *only* go **down**, never right, so the number of ways to reach the goal from `(r, last)` must equal the number of ways from `(r+1, last)`—provided the current cell is free. |

---

#### How this kills paths when the column is blocked

1. **Hit an obstacle in the last column**  
   When the loop reaches a row `k` where `obstacleGrid[k][last] == 1`, the `if` guard fails and `curr[last]` stays at its default `0`.

2. **Propagate the zero upward**  
   - We finish that row, then assign `prev = curr`.  
   - In the next iteration (row `k‑1`), `prev[last]` is already `0`, so `curr[last] = prev[last] = 0`.  
   - The zero keeps bubbling up until the top row is reached.

Result: every cell **above** the blocking obstacle in that column now contains `0`, correctly signalling that no path can bypass a vertical wall of obstacles.

---

#### The same idea handles a complete **row** of obstacles

While filling the rest of the row we use

```python
curr[c] = curr[c+1] + prev[c]   # only if grid[r][c] == 0
```

- When an obstacle sits at column `j`, the `if` guard fails → `curr[j]` stays `0`.
- Cells **left** of `j` need `curr[j]` (their right neighbour) in their sum.  
  Because `curr[j]` is `0`, every cell to the left also turns `0`, wiping out any path that would have crossed that horizontal wall.

---

So that single ternary assignment guarantees the two essential base‑cases for the dynamic programme:

- **Bottom‑right seed = 1** *(if open)*  
- **All higher rows in the last column inherit from the row below*—and inherit a zero as soon as an obstacle appears, permanently shutting off the column above it.

Hence an entire blocked row or column automatically collapses the corresponding DP values to zero, making the solution robust for every grid layout.


### Longest Common Subsequence[[Link](https://neetcode.io/problems/longest-common-subsequence)]
```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:

```