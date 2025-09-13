## *2226. Maximum Candies Allocated to K Children[[Link](https://leetcode.com/problems/maximum-candies-allocated-to-k-children/description/)]

- video explaination[[Link](https://neetcode.io/solutions/maximum-candies-allocated-to-k-children)]

```py
"""
Question Understanding
- Input:
    - `candies`: 0-index integer array
    - `k`: integer, indicates the number of children and each child should get same num of candies
- Rules:
    - each pile of candies[i], can divided into any number of sub piles
    - cannot merge two piles together
    - there is allowed to have leftovers, and each cild can only get one whole pile maximum, cannot fill candies from other piles after that
- Output:
    - Return the max number of candies each child can get

Clarification:
- Can the candies = [] and k != 0?
- Does the input `candies` in ascening order?

Assumptions:
- 1 <= len(candies) <= 10^5
- 1 <= candies[i] <= 10^7
- 1 <= k <= 10^12
- Always integers, no floats
- Valid input arrays

Cases:
- candies = [5, 8, 6], k = 3, ret: 5
- candies = [1000], k = 5, ret: 200

Brute Force Approach:
- Try every possible size m from 1 to max(candies)
- For each m, compute total pieces
- If total pieces >= k, keep track of feasible m
- Complexity: O(n * max(candies)) — too slow

Simple Opratoins
- sort the `candnies` into ascending order
- midpoint calculations m = l + (r - l) // 2

Approach:
- Algo Analysis: Time o(n log())
"""

class Solution:
    def maximumCandies(self, candies: List[int], k: int) -> int:
        total = sum(candies)
        res = 0

        l, r = 1, total // k
        while l <= r:
            m = l + (r - l) // 2
            count = 0
            for c in candies:
                if c >= m:
                    count += c // m
            if count >= k:
                res = m
                l = m + 1
            else:
                r = m - 1
        return res
```

## *2616. Minimize the Maximum Difference of Pairs[[Link](https://leetcode.com/problems/minimize-the-maximum-difference-of-pairs/)]

- video explaination[[Link](https://neetcode.io/solutions/minimize-the-maximum-difference-of-pairs)]

```py
"""
Question Understanding:
- Input:
    - `nums`: 0-index integr array
    - `p: integer
- Defnition:
    - difference of a pair = abs(nums[i] - nums[j])
- Objective:
    - for each time, find the p pairs of indices, and each pair, find the diff from small to large, 
    - and among these p differences, take the maximum difference.
- Output:
    - max difference between these pairs

Assumptions:
- 1 <= nums.length <= 10^5
- 1 <= p <= (nums.length) / 2
- 1 <= nums[i] <= 10^5

Cases:
- nums = [1], p = 1, ret: 0
- nums = [1], p = 0, ret: (not considerd)
- nums = [2, 1, 3], p = 1, (can nums.length odd ?)

Genral Idea:
- The origin indeces of elements doesn't matter
    - sort the `nums` into ascending order
- Binary Search Approach
    - calcuate the mid point
    - the mid point needs to meet some condition
    - if meet codition, shift r = m - 1 or l = m + 1
- Things needs to work with:
    - What is the search range?
    - What conditions should check?
    - How to update the final result?

Approach:
- Algo Analysis: Time: O(n log n), Space: O(1)
"""

class Solution:
    def minimizeMax(self, nums: List[int], p: int) -> int:
        if p == 0:
            return 0

        def is_valid(threshold):
            i, count = 0, 0
            while i < len(nums) - 1:
                if abs(nums[i] - nums[i + 1]) <= threshold:
                    count += 1
                    i += 2
                else:
                    i += 1
                if count == p:
                    return True
            return False
        
        nums.sort()
        l, r = 0, nums[-1] - nums[0] # smallest and maximum allowed differences
        res = nums[-1] - nums[0]
        while l <= r:
            m = l + (r - l) // 2
            if is_valid(m):
                res = m
                r = m - 1
            else:
                l = m + 1
        return res
```

## 2064. Minimized Maximum of Products Distributed to Any Store[[Link](https://leetcode.com/problems/minimized-maximum-of-products-distributed-to-any-store/)]

```py
"""
Question Understanding:
- Input:
    - integer `n`: number of special retail store
    - integer `m`: number of product types
    - integer arr `quantities`
        - quantities[i] : number of products under ith product type
- Objective:
    - distribute all products within `quantities`
    - give each store only one product type but any amout
    - trying to distributed as evenly as possible
- Output
    - return the minimal requirement of the maximum number such that (distribute all products within `quantities`)

Assumptions:
- 1 <= m <= n <= 10^5
- m == quantities.length
- 1 <= quantities[i] <= 10^5

Edge Cases:
- n = 1, quantities = [X] → output = X
- quantities = [1,1,1,1], n=10 → output = 1
- Very large quantities with large n
- quantities has one large and many small → balancing matters

Underlying Simple Operations:
- Division ceil(q / limit) → number of stores needed for product q if each store can take at most limit
- Summation across product types → total stores needed for a candidate limit
- Binary search for smallest limit such that total stores needed ≤ n

Brute Force Approach:
- Start with maximum quantity = max(quantities)
- Try decreasing limits from max down to 1, check if possible
- For each limit, calculate how many stores required
- Return first feasible limit
- Complexity O(max(quantities) * m) → too large (up to 1e5 * 1e5)

My Approach & Design:
Approach:
- Algo Analysis: Time O(m log(max_q)), Space O(1)
- Clarify variables needed:
    - left, right: search range for max load
    - mid: candidate max load
    - total_stores_needed: sum(ceil(q / mid) for q in quantities)
- Maintain:
    - quantities (sorted or unsorted, doesn’t matter for calculation)
- Steps:
    - Step 1: Initialize left=1, right=max(quantities)
      - Reasoning: min load cannot be less than 1, cannot exceed largest quantity
    - Step 2: Binary search while left < right
      - Reasoning: search space monotonic
    - Step 3: Compute stores needed for mid
        - total = 0
        - for q in quantities: total += ceil(q / mid)
        - If total ≤ n → feasible → shrink right
        - Else → infeasible → left = mid+1
      - Reasoning: if we can satisfy with mid, we can also satisfy with larger mid
    - Step 4: At the end, left=right=answer
      - Reasoning: binary search invariant guarantees minimal feasible limit
"""

class Solution:
    def minimizedMaximum(self, n: int, quantities: List[int]) -> int:
        def can_distribute(limit):
            total = 0
            for q in quantities:
                total += (q + limit - 1) // limit  # ceil division
                if total > n:
                    return False
            return total <= n
        
        l, r = 1, max(quantities)
        res = 0
        while l <= r:
            m = l + (r - l) // 2
            if can_distribute(m):
                res = m
                r = m - 1
            else:
                l = m + 1
        return res
```