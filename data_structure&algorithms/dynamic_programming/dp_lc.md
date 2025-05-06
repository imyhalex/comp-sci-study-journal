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

# or in optimized
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        dp = [0] * (len(text2) + 1)

        rows, cols = len(text1), len(text2)
        for r in range(rows - 1, -1, -1):
            curr = [0] * (len(text2) + 1)
            for c in range(cols - 1, -1, -1):
                if text1[r] == text2[c]:
                    curr[c] = dp[c + 1] + 1
                else:
                    curr[c] = max(dp[c], curr[c + 1])
            dp = curr

        return dp[0]
        
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

### *494. Target Sum[[Link](https://leetcode.com/problems/target-sum/description/)]

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
# Time Complexity: O(n * m)
# Space Complexity: O(n * m)
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        dp = [defaultdict(int) for _ in range(len(nums) + 1)]

        dp[0][0] = 1 # (0 element, 0 sum) -> 1 way
                     # 1 way to zero with first 0 elements
        
        for i in range(len(nums)):
            for curr_sum, count in dp[i].items():
                dp[i + 1][curr_sum + nums[i]] += count
                dp[i + 1][curr_sum - nums[i]] += count

        return dp[len(nums)][target]

# or optimized in
# Time Complexity: O(n * m)
# Space Complexity: O(m)
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        dp = defaultdict(int)
        dp[0] = 1

        for num in nums:
            next_dp = defaultdict(int)
            for total, count in dp.items():
                next_dp[total + num] += count
                next_dp[total - num] += count
            dp = next_dp
            
        return dp[target]
```

### 474. Ones and Zeroes[[Link](https://leetcode.com/problems/ones-and-zeroes/description/)]

- video explaination[[Link](https://neetcode.io/solutions/ones-and-zeroes)]

```python
# memoization
# Time Complexity: O(n * m * N); Space Complexity: O(n * m *N)
class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        # memoization
        dp = {}

        def dfs(i, m, n):
            if i == len(strs):
                return 0
            
            if (i, m, n) in dp:
                return dp[(i, m, n)]

            m_cnt, n_cnt = strs[i].count("0"), strs[i].count("1")
            # include the string at index i or not include the string at index i
            dp[(i, m, n)] = dfs(i + 1, m, n)
            if m_cnt <= m and n_cnt <= n:
                dp[(i, m, n)] = max(dp[(i, m, n)], 1 + dfs(i + 1, m - m_cnt, n - n_cnt))
            return dp[(i, m, n)]
        
        return dfs(0, m, n)


# bottom-up dp
# Time Complexity: O(n * m * N); Space Complexity: O(n * m * N)
class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        dp = defaultdict(int) 

        for i in range(len(strs)):
            s = strs[i]
            m_cnt, n_cnt = s.count("0"), s.count("1")
            for m in range(0, m + 1):
                for n in range(0, n + 1):
                    if m_cnt <= m and n_cnt <= n:
                        dp[(i, m, n)] = max(1 + dp[(i - 1, m - m_cnt, n - n_cnt)], dp[(i - 1, m, n)])
                    else:
                        dp[(i, m, n)] = dp[(i - 1, m, n)]
        return dp[(len(strs) - 1, m, n)]

# bottom-up optimized
# Time Complexity: O(n * m * N); Space Complexity: O(n * m + N)
class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        dp = defaultdict(int) 

        for s in strs:
            m_cnt, n_cnt = s.count("0"), s.count("1")
            for m_i in range(m, m_cnt - 1, -1):
                for n_j in range(n, n_cnt - 1, -1):
                    dp[(m_i, n_j)] = max(1 + dp[(m_i - m_cnt, n_j - n_cnt)], dp[(m_i, n_j)])
        
        return dp[(m, n)]
```

### 1049. Last Stone Weight II[[Link](https://leetcode.com/problems/last-stone-weight-ii/description/)]
- video explaination[[Link](https://neetcode.io/solutions/last-stone-weight-ii)]

```python
# memoization
# Time Complexity: O(n * m); Space Complexity: O(n * m)
class Solution:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        dp = defaultdict(int) 

        stone_sum = sum(stones)
        target = ceil(stone_sum) # or (stoneSum + 1) // 2

        def dfs(i, total):
            if total >= target or i == len(stones):
                return abs(total - (stone_sum - total))
            if (i, total) in dp:
                return dp[(i, total)]
            
            dp[(i, total)] = min(dfs(i + 1, total), dfs(i + 1, total + stones[i]))
            return dp[(i, total)]
        
        return dfs(0, 0)

# bottom-up dp optimized
# Time: O(n * m); Space: O(m)
# more neet way
class Solution:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        stoneSum = sum(stones)
        target = stoneSum // 2
        dp = [0] * (target + 1)

        for stone in stones:
            for t in range(target, stone - 1, -1):
                dp[t] = max(dp[t], dp[t - stone] + stone)

        return stoneSum - 2 * dp[target]

# or
class Solution:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        total = sum(stones)
        target = total // 2 

        dp = [False] * (target + 1)
        dp[0] = True

        for s in stones:
            # traverse backward to avoid 
            for j in range(target, s - 1, -1):
                if dp[j - s]:
                    dp[j] = True # if j - stone is reachable, j is also reachable
        
        # find the largest j <= target where dp[j] is True
        for j in range(target, -1, -1):
            if dp[j]:
                return total - 2 * j
        
        return 0

```


### 983. Minimum Cost For Tickets[[Link](https://leetcode.com/problems/minimum-cost-for-tickets/description/)]

- video explaination[[Link](https://neetcode.io/solutions/minimum-cost-for-tickets)]

__Top Down__
```python
class Solution:
    def mincostTickets(self, days: List[int], costs: List[int]) -> int:
        """
        c = {
            1: cost[0],
            7: cost[1],
            30: cost[2]
        }
        """
        dp = {} 

        def dfs(i):
            if i == len(days):
                return 0
            
            if i in dp:
                return dp[i]

            dp[i] = float("inf")
            j = i
            for cost, duration in zip(costs, [1, 7, 30]):
                while j < len(days) and days[j] < days[i] + duration:
                    j += 1
                dp[i] = min(dp[i], cost + dfs(j))
            
            return dp[i]
        
        return dfs(0)
```

__Bottom Up__
```python
class Solution:
    def mincostTickets(self, days: List[int], costs: List[int]) -> int:
        dp = [0] * (len(days) + 1)

        for i in range(len(days) - 1, -1, -1):
            j = i
            dp[i] = float('inf')
            for cost, duration in zip(costs, [1, 7, 30]):
                while j < len(days) and days[j] < days[i] + duration:
                    j += 1
                dp[i] = min(dp[i], cost + dp[j])
        return dp[0]
```