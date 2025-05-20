# Hashing in LC

## 217. Contains Duplicate[[Link](https://leetcode.com/problems/contains-duplicate/)]
- video explaination[[Link](https://neetcode.io/problems/duplicate-integer)]

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        hash_set = set()
        for num in nums:
            if num in hash_set:
                return True
            hash_set.add(num)
        return False
```

## 219. Contains Duplicate II[[Link](https://leetcode.com/problems/contains-duplicate-ii/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/contains-duplicate-ii)]
- hint: this is a fixed size sliding window problem

```python
class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        window = set()
        # two pointers left and right
        l = 0
        for r in range(len(nums)):
            if r - l > k:
                window.remove(nums[l])
                l += 1
            if nums[r] in window:
                return True
            window.add(nums[r])
        return False
```

## 1. Two Sum[[Link](https://leetcode.com/problems/two-sum/description/?envType=study-plan-v2&envId=top-interview-150)]
- video explaination[[Link](https://neetcode.io/problems/two-integer-sum)]
- important: return indices only if diff offset is in hash_map and the offset is not equal to the current one
```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hash_map = {}

        for i, n in enumerate(nums):
            hash_map[n] = i
        
        for i, n in enumerate(nums):
            diff = target - n
            if diff in hash_map and hash_map[diff] != i:
                return [i, hash_map[diff]]
```