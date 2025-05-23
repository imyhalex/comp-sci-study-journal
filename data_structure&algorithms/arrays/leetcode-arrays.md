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

## *560. Subarray Sum Equals K[[Link](https://leetcode.com/problems/subarray-sum-equals-k/description/)]
- video explaination[[Link](https://neetcode.io/problems/subarray-sum-equals-k)]
- hint: 
```python
# time & space: O(n)
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # hashmap: (prefix, count) pair
        # default (0, 1) -> prefix=0, count=1
        res = 0
        curr_sum = 0
        prefix_sum = {0: 1}

        for num in nums:
            curr_sum += num
            diff = curr_sum - k
            # lookup in the hashmap
            res += prefix_sum.get(diff, 0)
            prefix_sum[curr_sum] = 1 + prefix_sum.get(curr_sum, 0)
        
        return res
```

## 271. Encode and Decode Strings[[Link](https://leetcode.com/problems/encode-and-decode-strings/description/)]

- video explaination[[Link](https://neetcode.io/problems/string-encode-and-decode)]

```python
# time: O(m)
# space: O(m + n)
class Codec:
    def encode(self, strs: List[str]) -> str:
        """Encodes a list of strings to a single string.
        """
        res = ""
        for s in strs:
            res += str(len(s)) + "#" + s
        return res
        

    def decode(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings.
        """
        res = []
        i = 0

        while i < len(s):
            j = i
            while s[j] != "#":
                j += 1
            length = int(s[i:j]) # slice out the number
            i = j + 1
            j = i + length
            res.append(s[i:j])
            i = j # update the i to the next num

        return res


# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.decode(codec.encode(strs))
```

## 36. Valid Sudoku[[Link](https://leetcode.com/problems/valid-sudoku/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/valid-sudoku)]

```python
# time & space: O(n ^ 2)
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = defaultdict(set)
        cols = defaultdict(set)
        square = defaultdict(set) # key = (r // 3, c // 3)

        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    continue

                if (board[r][c] in rows[r] or
                    board[r][c] in cols[c] or 
                    board[r][c] in square[(r // 3, c // 3)]):
                    return False

                cols[c].add(board[r][c])
                rows[r].add(board[r][c])
                square[(r // 3, c // 3)].add(board[r][c])

        return True
```

## 347. Top K Frequent Elements[[Link](https://leetcode.com/problems/top-k-frequent-elements/description/)]
- video explaination[[Link](https://neetcode.io/problems/top-k-elements-in-list)]
- concepts: hash table, bucket sort
- hint: a hashmap to record the num: freqnecy pair

```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = {}
        freq = [[] for _ in range(len(nums) + 1)]

        # feed in the count hashmap and take record for its freqency
        # for each num, check if it is in hashmap, then 1 + num or 0 
        for num in nums:
            count[num] = 1 + count.get(num, 0)

        # bucket sort part
        # take out each num, frequency (or num, cnt) pair from the hashmap
        for num, cnt in count.items():
            freq[cnt].append(num)

        res = []
        for i in range(len(freq) - 1, 0, -1):
            for num in freq[i]:
                res.append(num)
                if len(res) == k:
                    return res
        return None
```

## 125. Valid Palindrome[[Link](https://leetcode.com/problems/valid-palindrome/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Linnk](https://neetcode.io/problems/is-palindrome)]
```python
# first way: reverse string
# time: O(n); space: O(n)
class Solution:
    def isPalindrome(self, s: str) -> bool:
        new_str = ""
        for c in s:
            if c.isalnum():
                new_str += c.lower()
        return new_str == new_str[::-1]

# second way: two pointer
# time: O(n); space: O(1)
class Solution:
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            # because we need to skip non alpha-numerical characters, use while loop
            while l < r and not self.is_alphanum(s[l]):
                l += 1
            while l < r and not self.is_alphanum(s[r]):
                r -= 1
            # if left pointer not equals to right pointer
            # return false immediately
            if s[l].lower() != s[r].lower():
                return False
            # increment normally
            l += 1
            r -= 1
        return True

    # maybe interviewer wants you not using .isalnum()
    def is_alphanum(self, c) -> bool:
        return (
            (ord('A') <= ord(c) <= ord('Z')) or 
            (ord('a') <= ord(c) <= ord('z')) or 
            (ord('0') <= ord(c) <= ord('9'))
        )
```