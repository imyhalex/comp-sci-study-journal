# Prefix Sum[[linnk](https://neetcode.io/courses/advanced-algorithms/4)]
- Q: Given an array of values, design a data structure that can query the sum of a subarray of the values.

```python
class PrefixSum:

    def __init__(self, nums):
        self.prefix = []
        total = 0
        for num in nums:
            total += num
            self.prefix.append(total)
    
    def range_sum(self, l, r):
        pre_right = self.prefix[r]
        pre_left = self.prefix[l - 1] if l > 0 else 0
        return (pre_right - pre_left)
```