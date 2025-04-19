# Dynamic Programming

__What is dynamic programming?__
- Simply put, it is an optimized version of recursion.
- It takes a big problem and solves it by breaking it down into smaller problems. 
- he reason we say it is optimized recursion is because it is often more optimal when it comes to time and space.

## 1-Dimension DP[[Link](https://neetcode.io/courses/dsa-for-beginners/32)]


__Top Dow Approach(Memorization)__
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

__Bottom Up Approach(Tabulation)__
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
## 2-Dimension DP

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