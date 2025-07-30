## *152. Maximum Product Subarray[[Link](https://leetcode.com/problems/maximum-product-subarray/description/)]

- video explaination[[Link](https://neetcode.io/problems/maximum-product-subarray?list=neetcode250)]

```python
# time: O(n); space: O(1)
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        res = max(nums)
        curr_max, curr_min = 1, 1

        for n in nums:
            if n == 0:
                curr_max, curr_min = 1, 1
                continue 
            
            tmp = n * curr_max
            curr_max = max(n * curr_max, n * curr_min, n) # [-1, 8], then choose 8
            curr_min = min(tmp, n * curr_min, n) # [-1, -8], then choose -8
            res = max(res, curr_max, curr_min)
        
        return res
```