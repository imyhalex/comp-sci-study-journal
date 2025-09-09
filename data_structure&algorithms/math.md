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

## 779. K-th Symbol in Grammar[[Link](https://leetcode.com/problems/k-th-symbol-in-grammar/description/)]

```py
"""
Question Understanding:
- Input:
    - `n`: number of rows
    - `k`: the k index (1-index) element at nth row
- Ouput:
    - kth symbol in the nth row
- Rule:
    - Row 1: "0"
    - Row 2: replace 0 → "01"
    - Row 3: replace each char: "01" → "0110"
    - Row 4: replace each char: "0110" → "01101001"

Assumptions:
- 1 <= n <= 40
- 1 <= k <= 2 ^(n - 1) and all input k are valid

Cases:
- n = 1, k = 1 -> ret: 0
- k is excatly half of the row length

Approach:
- Algo Analysis: Time O(n), Space O(n)
- Simple Operations:
    - Determine the value of kth element by tracing back to previous rows
    - Identify parent index in previous row
    - Apply transformation rule:
        - If parent is 0 -> children [0, 1]
        - If parent is 1 -> children [1, 0]
    - Recursion mapping
- Maintain:
    - Base case: n = 1 -> return 0
- Steps:
    - At row n, length = 2 ^ (n - 1)
    - Parent of kth element is at index (k + 1) // 2 in row n - 1
    - Recursively get parent's value
    - Determin child:
        - If parent = 0 → children [0,1]
        - If parent = 1 → children [1,0]
        - If k is odd -> first child
        - If k is even -> second child
"""

class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        if n == 1:
            return 0
        
        parent = self.kthGrammar(n - 1, (k + 1) // 2)
        # when parent is 0 the 1 appear in even postion, when parent is 1 the 1 appear in odd position
        if parent == 0:
            return 0 if k % 2 == 1 else 1
        else:
            return 1 if k % 2 == 1 else 0
```