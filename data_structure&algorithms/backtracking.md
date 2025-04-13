# Backtracking Problems

## Subsets

- Explain[[Link](https://neetcode.io/courses/advanced-algorithms/11)]
- Time: O(n * 2^n), Space O(n)

### Distinct Element Subset
```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        subsets, currset = [], []
        self.get_subsets(0, nums, subsets, currset)
        return subsets
    
    def get_subsets(self, idx, nums, sub, curr):
        if idx >= len(nums):
            sub.append(curr.copy())
            return

        curr.append(nums[idx])
        self.get_subsets(idx + 1, nums, sub, curr)
        curr.pop()
        self.get_subsets(idx + 1, nums, sub, curr)
```

### Subsets - non-distinct elements
```python
class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        subsets, currset = [], []
        self.get_subsets(0, nums, subsets, currset)
        return subsets
    
    def get_subsets(self, idx, nums, sub, curr):
        if idx >= len(nums):
            sub.append(curr.copy())
            return

        curr.append(nums[idx])
        self.get_subsets(idx + 1, nums, sub, curr)
        curr.pop()

        while idx + 1 < len(nums) and nums[idx] == nums[idx + 1]:
            idx += 1
        self.get_subsets(idx + 1, nums, sub, curr)
```

## Combination
- Time Complexity: O(k * 2^n)

### 1. Trivial Approach
```python
def combination(n, k):
    combs, curr = [], []
    get_combs(1, curr, combs, n, k)
    return combs

def get_combs(i, curr, combs, n, k):
    if len(curr) == k:
        combs.append(curr.copy())
        return
    if i > n:
        return
    
    curr.appen(i)
    get_combs(i + 1, curr, combs, n, k)
    curr.pop()

    get_combs(i + 1, curr, combs, n, k)
```

### 2. Optimized Approcah
- Time Complexity: O(k * C(n, k))
```python
def combination(n, k):
    combs, curr = [], []
    get_combs(1, curr, combs, n, k)
    return combs

def get_combs(i, curr, combs, n, k):
    if len(curr) == k:
        combs.append(curr.copy())
        return
    if i > n:
        return
    
    for j in range(i, n + 1):
        curr.append(j)
        get_combs(j + 1, curr, combs, n, k)
        curr.pop()
```


## Some LC Problems
### 77. Combinations[[Link](https://leetcode.com/problems/combinations/description/)]
```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        combs, curr = [], []
        self.get_combs(1, curr, combs, n, k)
        return combs
    
    def get_combs(self, i, curr, combs, n, k):
        if len(curr) == k:
            combs.append(curr.copy())
            return 
        if i > n:
            return 
        
        for j in range(i, n + 1):
            curr.append(j)
            self.get_combs(j + 1, curr, combs, n, k)
            curr.pop()
```

### Combination Sum[[Link](https://neetcode.io/problems/combination-target-sum)]
```python
class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        combs, curr = [], []
        self.get_combs_sum(0, curr, combs, nums, target, 0)
        return combs
    
    def get_combs_sum(self, i, curr, combs, nums, target, total):
        if total == target:
            combs.append(curr.copy())
            return 
        if i >= len(nums) or total > target:
            return
        
        curr.append(nums[i])
        self.get_combs_sum(i, curr, combs, nums, target, nums[i] + total)
        curr.pop()

        self.get_combs_sum(i + 1, curr, combs, nums, target, total)
        

```

### 17. Letter Combinations of a Phone Number[[Link](https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/?envType=study-plan-v2&envId=top-interview-150)]

```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        # construct a hash tablb
        table = {
            str(k): v 
            for k, v in zip(range(2, 10), ["abc", "def", "ghi", "jkl", "mno", "qprs", "tuv", "wxyz"])
        }
        combs, curr = [], ""
        self.get_letter_combs(0, curr, combs, digits, table)
        return combs
    
    def get_letter_combs(self, i, curr, combs, digits, table):
        if len(curr) == len(digits):
            combs.append(curr)
            return
        
        for letter in table[digits[i]]:
            self.get_letter_combs(i + 1, curr + letter, combs, digits, table)
```