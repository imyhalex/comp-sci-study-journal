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
## Unbounded Knapsack[[Link](https://neetcode.io/courses/advanced-algorithms/19)]

- Unlike 0/1 knapscak, which only allowed to include each item at most once, the unbounded knapsack has no limit on how many times we can include an item

```text
Q: Given a list of N items, and a backpack with a limited capacity, return the maximum total profit that can be contained in the backpack. 
The i-th item's profit is profit[i] and its weight is weight[i]. Assume you can have an unlimited number of each item available.
```

### Brute Force Approach
```python
# Brute force Solution
# Time: O(2^c), Space: O(c)
# Where c is the capacity.

def dfs(profit, weight, capacity):
    return dfsHelper(0, profit, weight, capacity)

def dfsHelper(i, profit, weight, capacity):
    if i == len(profit):
        return 0
    
    # skip i
    maxProfit = dfsHelper(i + 1, profit, weight, capacity)

    # include i
    newCap = capacity - weight[i]
    if newCap >= 0:
        p = profit[i] + dfsHelper(i, profit, weight, newCap)
        # compute the max
        maxProfit = max(maxProfit, p)
    
    return maxProfit


# compare to 0/1 knapsack
# def dfs(profit, weight, capacity):
#     return dfsHelper(0, profit, weight, capacity)

# def dfsHelper(i, profit, weight, capacity):
#     if i == len(profit):
#         return 0

#     # Skip item i
#     maxProfit = dfsHelper(i + 1, profit, weight, capacity)

#     # Include item i
#     newCap = capacity - weight[i]
#     if newCap >= 0:
#         p = profit[i] + dfsHelper(i + 1, profit, weight, newCap)
#         # Compute the max
#         maxProfit = max(maxProfit, p)

#     return maxProfit
```

### Top Down
```python
# Memoization Solution
# Time: O(n * m), Space: O(n * m)
# Where n is the number of items & m is the capacity.
def memoization(profit, weight, capacity):
    # A 2d array, with N rows and M + 1 columns, init with -1's
    # This is our problem space - two-dimensional grid
    N, M = len(profit), capacity
    cache = [[-1] * (M + 1) for _ in range(N)]
    return memoHelper(0, profit, weight, capacity, cache)

def memoHelper(i, profit, weight, capacity, cache):
    if i == len(profit):
        return 0
    if cache[i][capacity] != -1:
        return cache[i][capacity]

    # Skip item i
    cache[i][capacity] = memoHelper(i + 1, profit, weight, capacity, cache)
    
    # Include item i
    newCap = capacity - weight[i]
    if newCap >= 0:
        p = profit[i] + memoHelper(i, profit, weight, newCap, cache)
        # Compute the max
        cache[i][capacity] = max(cache[i][capacity], p)

    return cache[i][capacity]
```

### Bottom Up
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
                include = profit[i] + dp[i][c - weight[i]]
            dp[i][c] = max(skip, include)
    return dp[n - 1][m]
```

### Bottom Up (Optimized)
```python
# Memory optimized Dynamic Programming Solution
# Time: O(n * m), Space: O(m)
def optimizedDp(profit, weight, capacity):
    n, m = len(profit), capacity
    dp = [0] * (m + 1)

    for c in range(m + 1):
        if weight[0] <= c:
            dp[c] = profit[0]

    for i in range(1, n):
        curr = [0] * (m + 1)
        for c in range(1, m + 1):
            skip = dp[c]
            include = 0
            if c - weight[i] >= 0:
                include = profit[i] + curr[c - weight[i]]
            curr[c] = max(include, skip)
        dp = curr
    return dp[m]

# compare to 0/1 knapsack
# def dp_optimized(profit, weight, capacity):
#     n, m = len(profit), capacity
#     dp = [0] * (m + 1)

#     # fill the first row to reduce edge cases
#     for c in range(m + 1):
#         if weight[0] <= c:
#             dp[c] = profit[0]
    
#     for i in range(1, n):
#         curr = [0] * (m + 1)
#         for c in range(1, m + 1):
#             # skip
#             skip = dp[c]
#             # or include
#             include = 0
#             if c - weight[i] >= 0:
#                 include = profit[i] + dp[c - weight[i]]
#             curr[c] = max(skip, include)
#         dp = curr
#     return dp[m]
```

## Longest Common Sequence[[Link](https://neetcode.io/courses/advanced-algorithms/20)]

- Q: Given two stirng s1 and s2, find the length of the longest common subsequence between two strings
