## 231. Power of Two[[Link](https://leetcode.com/problems/power-of-two/description/)]

```python
class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return n != 0 and (n & (n - 1)) == 0

# or
class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        res = 0
        x = 0
        while res < n:
            res = 2 ** x
            x += 1
        
        return res == n if n != 0 else False
```

## 869. Reordered Power of 2[[Link](https://leetcode.com/problems/reordered-power-of-2/description/?envType=daily-question&envId=2025-08-10)]

```python
# 
class Solution:
    def reorderedPowerOf2(self, n: int) -> bool:
        """
        backtracking
        permutation
        """
        def signature(x):
            return tuple(sorted(str(x)))
        
        target = signature(n)

        for i in range(31):
            if signature(1 << i) == target:
                return True
        return False
```