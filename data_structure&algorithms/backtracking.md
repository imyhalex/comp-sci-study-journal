# Subsets

- Explain[[Link](https://neetcode.io/courses/advanced-algorithms/11)]
- Time: O(n * 2^n), Space O(n)

## Distinct Element Subset
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

## Subsets - non-distinct elements
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