## 307. Range Sum Query - Mutable[[Link](https://leetcode.com/problems/range-sum-query-mutable/description/)]

- video explaination[[Link]()]

```python
class SegmentTree:
    def __init__(self, total, L, R):
        self.sum = total
        self.left = None
        self.right = None
        self.L = L
        self.R = R
    
    @staticmethod
    def build(nums, L, R):
        if L == R:
            return SegmentTree(nums[L], L, R)
        
        M = L + (R - L) // 2
        # intialize a root with a sum of 0, then will be recursively calculated
        root = SegmentTree(0, L, R)
        root.left = SegmentTree.build(nums, L, M)
        root.right = SegmentTree.build(nums, M + 1, R)
        root.sum = root.left.sum + root.right.sum
        return root
    
    def update(self, index, val):
        if self.L == self.R:
            self.sum = val
            return 

        M = self.L + (self.R - self.L) // 2
        if index <= M:
            self.left.update(index, val)
        else:
            self.right.update(index, val)
        self.sum = self.left.sum + self.right.sum
    
    def sum_range(self, l, r):
        if l == self.L and r == self.R:
            return self.sum
        
        M = self.L + (self.R - self.L) // 2
        if r <= M:
            return self.left.sum_range(l, r)
        elif l > M:
            return self.right.sum_range(l, r)
        else:
            return (self.left.sum_range(l, M) +
                    self.right.sum_range(M + 1, r))

class NumArray:

    def __init__(self, nums: List[int]):
        if nums:
            self.root = SegmentTree.build(nums, 0, len(nums) - 1)
        else:
            self.root = None

    def update(self, index: int, val: int) -> None:
        if self.root:
            self.root.update(index, val)

    def sumRange(self, left: int, right: int) -> int:
        if self.root:
            return self.root.sum_range(left, right)
        return 0


# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# obj.update(index,val)
# param_2 = obj.sumRange(left,right)
```