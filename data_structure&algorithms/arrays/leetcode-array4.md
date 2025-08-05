## 283. Move Zeroes[[Link](https://leetcode.com/problems/move-zeroes/description/?envType=study-plan-v2&envId=leetcode-75)]

- video explaination[[Link](https://neetcode.io/problems/move-zeroes?list=allNC)]

```python
# time: O(n); space: O(1)
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums) # range still need to scan
        l = 0
        
        while l < n:
            if nums[l] == 0:
                nums.append(nums[l])
                del nums[l]
                n -= 1
            else:
                l += 1
```