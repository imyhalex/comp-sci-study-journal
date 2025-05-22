# Arrays in LC

## 303. Range Sum Query - Immutable[[Link](https://leetcode.com/problems/range-sum-query-immutable/description/)]
- vide explaination[[Link](https://neetcode.io/solutions/range-sum-query-immutable)]

```python
class NumArray:

    def __init__(self, nums: List[int]):
        self.prefix = []
        total = 0
        for num in nums:
            total += num
            self.prefix.append(total)

    def sumRange(self, left: int, right: int) -> int:
        pre_right= self.prefix[right]
        pre_left = self.prefix[left - 1] if left > 0 else 0
        return (pre_right - pre_left)
```

## 304. Range Sum Query 2D - Immutable[[Link](https://leetcode.com/problems/range-sum-query-2d-immutable/description/)]
- video explaination[[Link](https://neetcode.io/solutions/range-sum-query-2d-immutable)]
- hint: prefix matrix, minus the left and the above + topleft (double delete, so add back in again)
```python
class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        rows, cols = len(matrix), len(matrix[0])
        self.prefix_matrix = [[0] * (cols + 1) for _ in range(rows + 1)] # add one row and col fill in zero to avoid edge cases

        for r in range(rows):
            prefix = 0
            for c in range(cols):
                prefix += matrix[r][c] # for each row
                above = self.prefix_matrix[r][c + 1]
                self.prefix_matrix[r + 1][c + 1] = prefix + above # for columns prefix, r + 1 for offset, c + 1 for increment

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        row1, col1, row2, col2 = row1 + 1, col1 + 1, row2 + 1, col2 + 1 # to offset the prefix matrix
        bottom_right = self.prefix_matrix[row2][col2]
        above = self.prefix_matrix[row1 - 1][col2]
        left = self.prefix_matrix[row2][col1 - 1]
        top_left = self.prefix_matrix[row1 - 1][col1 - 1]
        return bottom_right - above - left + top_left


# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# param_1 = obj.sumRegion(row1,col1,row2,col2)
```

## 724. Find Pivot Index[[Link](https://leetcode.com/problems/find-pivot-index/description/)]
- time complexity: O(n); space complexity: O(n)
- video explaination[[Link](https://neetcode.io/solutions/find-pivot-index)]
```python
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        # nums = [1,7,3,6,5,6]
        # prefix = [0]-[1,7,11,17,22,28]
        n = len(nums)
        prefix = [0] * (n + 1)

        # feed the prefix sum
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        # left=left sum; right=right sum
        for i in range(n):
            left = prefix[i]
            right = prefix[n] - prefix[i + 1]
            if left == right:
                return i
        return - 1
```

## 238. Product of Array Except Self[[Link](https://leetcode.com/problems/product-of-array-except-self/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/products-of-array-discluding-self)]

```python
# using extra memory
# time & space: O(n)
# class Solution:
#     def productExceptSelf(self, nums: List[int]) -> List[int]:
#         n = len(nums)
#         res = [0] * n
#         prefix = [0] * n
#         suffix = [0] * n

#         prefix[0] = suffix[n - 1] = 1 # set initial 1 else every product will be zero
#         for i in range(1, n):
#             prefix[i] = nums[i - 1] * prefix[i - 1]
#         for i in range(n - 2, -1, -1):
#             suffix[i] = nums[i + 1] * suffix[i + 1]
#         for i in range(n):
#             res[i] = prefix[i] * suffix[i]
#         return res

# memorize this version
# memory optimization
# time: O(n); space: O(1)
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1] * len(nums)

        prefix = 1
        for i in range(len(nums)):
            res[i] = prefix
            prefix *= nums[i]
        postfix = 1
        for i in range(len(nums) - 1, -1, -1):
            res[i] *= postfix
            postfix *= nums[i]
        return res
```