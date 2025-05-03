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
- Time Complexity get optimized to: O(n), and only use the array with size of 2, we can bring space complexity down to O(1)
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

# or
class Solution:
    def fib(self, n: int) -> int:
        if n < 2:
            return n
        
        dp = [0, 1]
        for i in range(2, n + 1):
            tmp = dp[1]
            dp[1] = dp[0] + dp[1]
            dp[0] = tmp
        
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

## 0/1 Knapsack[[Link](https://neetcode.io/courses/advanced-algorithms/18)]

- Idea:
    - given a bag/knapsack with a fixed capacity, along with some items' weights and profits we reap by choosing to put that item in the bag.
    - want to maximize the profit while also ensuring that our backpack doesn't run out of space. 
- The reason this algorithm is called 0/1 is because at each point, we can either choose to include an item or not include it - a binary decision.

```text
Q: Given a list of N items, and a backpack with a limited capacity, return the maximum total profit that can be contained in the backpack. The i-th 
item's profit is profit[i] and its weight is weight[i]. Assume you can only add each item to the bag at most once.
```

### Brute Force Approach
```python
# Brute force Solution
# Time: O(2^n), Space: O(n)
# Where n is the number of items.

def dfs(profit, weight, capacity):
    return dfsHelper(0, profit, weight, capacity)

def dfsHelper(i, profit, weight, capacity):
    if i == len(profit):
        return 0

    # Skip item i
    maxProfit = dfsHelper(i + 1, profit, weight, capacity)

    # Include item i
    newCap = capacity - weight[i]
    if newCap >= 0:
        p = profit[i] + dfsHelper(i + 1, profit, weight, newCap)
        # Compute the max
        maxProfit = max(maxProfit, p)

    return maxProfit
```

### Top-Down Approach(Memoization)
```python
# Memoization Solution
# Time: O(n * m), Space: O(n * m)
# Where n is the number of items & m is the capacity.

def memoization(profit, weight, capacity):
    # A 2d array, with N rows and M + 1 columns, init with -1's
    n, m = len(profit), capacity
    cache = [[-1] * (m + 1) for _ in range(len(n))]
    return memo_helper(0, profit, weight, capacity, cache)

def memo_helper(i, profit, weight, capacity, cache):
    if i == len(profit):
        return 0
    
    if cache[i][capacity] != -1:
        return cache[i][capacity]
    
    # skip item i
    cache[i][capacity] = memo_helper(i + 1, profit, weight, capacity, cache)

    # include item i
    new_cap = capacity - weight[i]
    if new_cap > 0:
        p = profit[i] + memo_helper(i + 1, profit, weight, new_cap, cache)
        # compute the max
        cache[i][capacity] = max(cache[i][capacity], p)
    
    return cache[i][capacity]
```

### Bottom-UP Approach
```python
# Dynamic Programming Solution
# Time: O(n * m), Space: O(n * m)
# Where n is the number of items & m is the capacity.

def dp(profit, weight, capacity):
    n, m = len(profit), capacity
    dp = [[0] * (m + 1) for _ in range(n)]

    # fill th first column and row to reduce edge cases
    for i in range(n):
        dp[i][0] = 0
    
    for c in range(m + 1):
        if weight[0] <= c:
            dp[0][c] = profit[0]
        
    for i in range(1, n):
        for c in range(1, m + 1):
            # either skip
            skip = dp[i - 1][c]
            # or include
            include = 0
            if c - weight[i] >= 0:
                include = profit[i] + dp[i - 1][c - weight[i]]
            dp[i][c] = max(skip, include)
    return dp[n - 1][m]
```

### Bottom-Up Approach(Optimized)
```python
# Memory optimized Dynamic Programming Solution
# Time: O(n * m), Space: O(m)

def dp_optimized(profit, weight, capacity):
    n, m = len(profit), capacity
    dp = [0] * (m + 1)

    # fill the first row to reduce edge cases
    for c in range(m + 1):
        if weight[0] <= c:
            dp[c] = profit[0]
    
    for i in range(1, n):
        curr = [0] * (m + 1)
        for c in range(1, m + 1):
            # skip
            skip = dp[c]
            # or include
            include = 0
            if c - weight[i] >= 0:
                include = profit[i] + dp[c - weight[i]]
            curr[c] = max(skip, include)
        dp = curr
    return dp[m]
```

## Some LC Problems

### 70. Climbing Stairs[[Link](https://leetcode.com/problems/climbing-stairs/description/)]

- video explaination[[Link](https://neetcode.io/solutions/climbing-stairs)]
- decision tree idea
```python
# recursion method:
class Solution:
    def climbStairs(self, n: int) -> int:
        def dfs(i):
            if i >= n:
                return i == n
            return dfs(i + 1) + dfs(i + 2)
        return dfs(0)  

# bottm-up dp: 
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

- video explaination[[Link](https://neetcode.io/solutions/house-robber)]

```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0

        if len(nums) == 1:
            return nums[0]
    
        dp = [0, 0] # dp[0] -> rob1, dp[1] -> rob2
        for n in nums:
            tmp = max(dp[0] + n, dp[1])
            dp[0] = dp[1] # override
            dp[1] = tmp # make sure dp[1] have most up-to-date num

        return dp[1]
```

### 322. *Coin Change[[Link](https://leetcode.com/problems/coin-change/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/solutions/coin-change)]
- unbounded knapsack(save for learning the topic later)
```python
# Time Complexity: O(amount * len(coin)); Space Complexity: O(amount)
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [amount + 1] * (amount + 1) # 'amount + 1' in [] is just to set default value
        dp[0] = 0 # base case

        for a in range(1, amount + 1):
            for c in coins:
                if a - c >= 0:
                    dp[a] = min(dp[a], 1 + dp[a - c])

        return dp[amount] if dp[amount] != amount + 1 else -1
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

```python
# solution in recursion
# Time complexity: O(t∗m^n); Space: O(n)
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:

        def dfs(i):
            if i == len(s):
                return True
            
            for w in wordDict:
                if ((i + len(w)) <= len(s) and s[i : i + len(w)] == w):
                    if dfs(i + len(w)):
                        return True
            return False
        
        return dfs(0)
```

- Video Explaination[[Link](https://neetcode.io/problems/word-break)]
- hint: set the position of string out of bound as True as a starting point; and traverse in reverse order
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

        # edge cases: if the destionation has obstacle or starting point conatins obstacle
        if obstacleGrid[rows - 1][cols - 1] or obstacleGrid[0][0]:
            return 0
            
        prev = [0] * cols
        for r in range(rows - 1, -1, -1):
            curr = [0] * cols
            # this part handle the last element for curr dp array
            if obstacleGrid[r][cols - 1] != 1:
                curr[cols - 1] = prev[cols - 1] if r < rows - 1 else 1
            
            for c in range(cols - 2, -1, -1):
                # this part handle the obstacle in the middle of the row in grid
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


### 1143. Longest Common Subsequence[[Link](https://leetcode.com/problems/longest-common-subsequence/description/)]

- video explaination[[Link](https://neetcode.io/solutions/longest-common-subsequence)]
- hint: if find common character, add on dp array in diagonal, it not, find the maximun num either from the right or below
```python
# recursion solution
# Time Complexity: O(2 ^ (m + n)); Space Complexity: O(m + n)
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        
        def dfs(i, j):
            if i == len(text1) or j == len(text2):
                return 0
            
            if text1[i] == text2[j]:
                return 1 + dfs(i + 1, j + 1)
            
            return max(dfs(i + 1, j), dfs(i, j + 1))

        return dfs(0, 0)


# DP in Bottom-Up 
# Time Complexity: O(n * m); Space Complexity: O(n * m)
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        dp = [[0 for j in range(len(text2) + 1)] for i in range(len(text1) + 1)]

        rows, cols = len(text1), len(text2)
        for i in range(rows - 1, -1, -1):
            for j in range(cols - 1, -1, -1):
                if text1[i] == text2[j]:
                    dp[i][j] = 1 + dp[i + 1][j + 1]
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
        
        return dp[0][0] 
```

### Partition Equal Subset Sum[[Link](https://neetcode.io/problems/partition-equal-subset-sum)]

- Video Explaination[[Link](https://www.youtube.com/watch?v=IsvocB5BJhw)]

__Brute-Force__
```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        if sum(nums) % 2 != 0:
            return False

        def dfs(i, target):
            if i >= len(nums):
                return target == 0
            if target < 0:
                return False
            
            return dfs(i + 1, target) or dfs(i + 1, target - nums[i])
        
        return dfs(0, sum(nums) // 2)
```

__Dynamic Programming__
```python
# Time complexity: O(n∗target); Space complexity: O(n∗target)
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        if sum(nums) % 2 != 0:
            return False

        n, target = len(nums), sum(nums) // 2
        dp = [[False] * (target + 1) for _ in range(n + 1)] # n + 1 for handle first item edge cases

        for i in range(n + 1):
            dp[i][0] = True

        for i in range(1, n + 1):
            for t in range(1, target + 1):
                if nums[i - 1] <= t:
                    dp[i][t] = (dp[i - 1][t] or dp[i - 1][t - nums[i - 1]])
                else:
                    dp[i][t] = dp[i - 1][t]
        return dp[n][target]
```
```python
# video-ish result

# Time complexity: O(n∗target); Space complexity: O(n∗target)
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        if sum(nums) % 2 != 0:
            return False
        
        n, target = len(nums), sum(nums) // 2
        dp = [[False] * (target + 1) for _ in range(n)]

        for i in range(n):
            dp[i][0] = True
        
        for t in range(target + 1):
            if nums[0] == t:
                dp[0][t] = True
        
        for i in range(1, n):
            for t in range(1, target + 1):
                not_take = dp[i - 1][t]
                take = False
                if t - nums[i] >= 0:
                    take= dp[i - 1][t - nums[i]]
                dp[i][t] = take or not_take
        return dp[n - 1][target]
```
```python
# optimized version

# Time complexity: O(n∗target); Space complexity: O(target)
class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        if sum(nums) % 2 != 0:
            return False

        n, target = len(nums), sum(nums) // 2
        dp = [False] * (target + 1)

        for t in range(target + 1):
            if nums[0] == t:
                dp[t] = True
        
        for i in range(1, n):
            curr = [False] * (target + 1)
            for t in range(1, target + 1):
                not_take = dp[t]
                take = False
                if t - nums[i] >= 0:
                    take = dp[t - nums[i]]
                curr[t] = take or not_take
            dp = curr
        return dp[target]

# or
# Time complexity: O(n∗target); Space complexity: O(target)
class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        if sum(nums) % 2 != 0:
            return False
        
        target = sum(nums) // 2
        dp = [False] * (target + 1)

        dp[0] = True
        for num in nums:
            for t in range(target, num - 1, - 1):
                dp[t] = dp[t] or dp[t - num]
        
        return dp[target]
```

### 494. Target Sum[[Link](https://leetcode.com/problems/target-sum/description/)]

- video explaination[[Link](https://neetcode.io/problems/target-sum)]
- hint: the 2d array should from -target to +target
```python
# Time complexity O(2^n)
# Space complextiy O(n)

class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:

        def dfs(i, total):
            if i == len(nums):
                return total == target
            
            return (dfs(i + 1, total + nums[i]) + dfs(i + 1, total - nums[i]))
        
        return dfs(0, 0)
```
__Memoization__
```python
# Time Complexity: O(n * m)
# Space Complexity: O(n * m)
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        dp = {} # (index, curr_sum) -> num of ways 

        def dfs(i, curr_sum):
            if (i, curr_sum) in dp:
                return dp[(i, curr_sum)]
            
            if i == len(nums):
                return curr_sum == target # True or False -> 1 or 0
            
            dp[(i, curr_sum)] = (
                dfs(i + 1, curr_sum + nums[i]) + dfs(i + 1, curr_sum - nums[i])
            )
            return dp[(i, curr_sum)]
        return dfs(0, 0)
```
__Bottom-UP__
```python
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        
```