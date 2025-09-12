## 2226. Maximum Candies Allocated to K Children[[Link](https://leetcode.com/problems/maximum-candies-allocated-to-k-children/description/)]

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