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
# brute force:
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        res = 0
        for i in range(len(nums)):
            sum = 0
            for j in range(i, len(nums)):
                sum += nums[j]
                if sum == k:
                    res += 1
        return res

# time & space: O(n)
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # hashmap: (prefix, count) pair
        # default (0, 1) -> prefix=0, count=1, default setup for prefix question
        res = 0
        curr_sum = 0
        prefix_sum = {0: 1}

        for num in nums:
            curr_sum += num
            diff = curr_sum - k
            # lookup the diff for exclude the "left" part of current prefix
            res += prefix_sum.get(diff, 0)
            # take record of current prefix sum
            # incrementing one for the current prefix we calculated
            prefix_sum[curr_sum] = 1 + prefix_sum.get(curr_sum, 0)
        
        return res

# same as
# https://leetcode.com/problems/contiguous-array/description/
# https://leetcode.com/problems/subarray-sum-equals-k/description/
# https://leetcode.com/problems/subarrays-with-k-different-integers/description/
# https://leetcode.com/problems/count-number-of-nice-subarrays/description/
# https://leetcode.com/problems/binary-subarrays-with-sum/description/
# https://leetcode.com/problems/subarray-product-less-than-k/description/
# https://leetcode.com/problems/count-subarrays-where-max-element-appears-at-least-k-times/description/
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

# j = i
# while s[j] != "#":
#     j += 1
# length = int(s[i:j]) # slice out the number
# i = j + 1
# j = i + length
# res.append(s[i:j])
# i = j # update the i to the next num

"""example
5#Hello5#World

j = i
5#Hello5#World
i
j

while s[j] != "#":
    j +=1
5#Hello5#World
i
 j

length = int(s[i:j])
[5] #Hello5#World
i
    j

i = j + 1
[5] #Hello5#World
     i
    j

j = i + length
[5] #Hello5#World
     i
          j

res.append(s[i:j])
[5] # [Hello] 5#World
       i
             j

i = j
[5] #[Hello] 5#World
             i
             j
"""


# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.decode(codec.encode(strs))
```

## 347. Top K Frequent Elements[[Link](https://leetcode.com/problems/top-k-frequent-elements/description/)]
- video explaination[[Link](https://neetcode.io/problems/top-k-elements-in-list)]
- concepts: hash table, bucket sort
- hint: a hashmap to record the num: freqnecy pair

```python
# time & space: O(n)
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

## 1. Two Sum[[Link](https://leetcode.com/problems/two-sum/description/?envType=study-plan-v2&envId=top-interview-150)]
- video explaination[[Link](https://neetcode.io/problems/two-integer-sum)]
- important: return indices only if diff offset is in hash_map and the offset is not equal to the current one
```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hash_map = {} # num -> num_idx
        # construct a hash_map
        for i, n in enumerate(nums):
            hash_map[n] = i
        # find the two sum using offset technique
        for i, n in enumerate(nums):
            diff = target - n
            if diff in hash_map and hash_map[diff] != i:
                return [i, hash_map[diff]]
```

## 167. Two Sum II - Input Array Is Sorted[[Link](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/two-integer-sum-ii)]

```python
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        l, r = 0, len(numbers) - 1
        while l < r:
            if numbers[l] + numbers[r] > target:
                r -= 1
            elif numbers[l] + numbers[r] < target:
                l += 1
            else:
                return [l + 1, r + 1]
                
        return []
```

## 15. 3Sum[[Link](https://leetcode.com/problems/3sum/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/three-integer-sum)]

```python
# Brute Force
# time: O(n^3); space: O(m)
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = set() # question asked the solution must not contains any duplicate triplets
        nums.sort()
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                for k in range(j + 1, len(nums)):
                    if nums[i] + nums[j] + nums[k] == 0:
                        res.add(tuple([nums[i], nums[j], nums[k]]))
        return [list(i) for i in res]

# two pointers
# time: O(n^2); space: O(1) or O(n) depending on the sorting algo
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        nums.sort()

        for i, num in enumerate(nums):
            # Notice that the solution set must not contain duplicate triplets.
            if i > 0 and num == nums[i - 1]:
                continue
            
            l, r = i + 1, len(nums) - 1
            while l < r:
                three_sum = num + nums[l] + nums[r]
                if three_sum > 0:
                    r -= 1
                elif three_sum < 0:
                    l += 1
                else:
                    res.append([num, nums[l], nums[r]])
                    # update the left pointer
                    l += 1
                    # also mind to jump over duplicate, so while loop
                    while nums[l] == nums[l - 1] and l < r: # l += 1 but should never pass r
                        l += 1
        return res
```

## 16. 3Sum Closest[[Link](https://leetcode.com/problems/3sum-closest/?envType=problem-list-v2&envId=two-pointers)]

```python
# time: O(n log n) + O(n²) = O(n²)
class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        res = nums[0] + nums[1] + nums[2] # initialize with the first triplets sum for compare contrast
        nums.sort()

        for i, num in enumerate(nums):
            l, r = i + 1, len(nums) - 1
            while l < r:
                three_sum = num + nums[l] + nums[r]
                if abs(three_sum - target) < abs(res - target):
                    res = three_sum

                if three_sum < target:
                    l += 1
                elif three_sum > target:
                    r -= 1
                else:
                    return target # return target for exact match
        return res
```

## *259. 3Sum Smaller[[Link](https://leetcode.com/problems/3sum-smaller/description/)]

```python
class Solution:
    def threeSumSmaller(self, nums: List[int], target: int) -> int:
        nums.sort()
        count = 0

        for i in range(len(nums) - 2):
            l, r = i + 1, len(nums) - 1
            while l < r:
                three_sum = nums[i] + nums[l] + nums[r]
                if three_sum < target:
                    count += r - l # All elements from l+1 to r are valid
                    l += 1
                else:
                    r -= 1
        return count
```

## 18. 4Sum[[Link](https://leetcode.com/problems/4sum/description/?envType=problem-list-v2&envId=two-pointers)]

- video explaination[[Link](https://neetcode.io/problems/4sum?list=neetcode250)]

```python
# time: O(n^3); space: O(1) or O(n) depends on sorting algo
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        res, quad = [], []

        def k_sum(k, start_idx, target):
            if k != 2:
                for i in range(start_idx, len(nums) - k + 1):
                    if i > start_idx and nums[i] == nums[i - 1]:
                        continue
                    
                    quad.append(nums[i])
                    k_sum(k - 1, i + 1, target - nums[i])
                    quad.pop()
                return
            # the previous one handeld two values for quad
            
            # base case, two sum 
            l, r = start_idx, len(nums) - 1
            while l < r:
                two_sum = nums[l] + nums[r]
                if two_sum < target:
                    l += 1
                elif two_sum > target:
                    r -= 1
                else:
                    res.append(quad + [nums[l], nums[r]])
                    l += 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1
        
        k_sum(4, 0, target)
        return res
```

## 392. Is Subsequence[[Link](https://leetcode.com/problems/is-subsequence/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/solutions/is-subsequence)]
```python
# two pointers way
# time: O(n + m); space: O(1)
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i = j = 0
        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                i += 1
            j += 1
        return i == len(s)
```
## *31. Next Permutation[[Link](https://leetcode.com/problems/next-permutation/description/?envType=problem-list-v2&envId=two-pointers)]

- explaination[[Link](https://neetcode.io/problems/next-permutation?list=allNC)]

```python
# time: O(n); space: O(1)
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        # 🔍 Step 1: Find the first "dip" from the right
        # This loop scans from right to left.
        # It finds the first number where the sequence stops increasing.
        # This means the sequence to the right of i is non-increasing (i.e., descending).
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1

        # 🔄 Step 2: If such a number exists (not fully descending), swap it
        # Now find the smallest number greater than nums[i] to the right of i.
        # Swap it with nums[i].
        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]

        # 🔃 Step 3: Reverse the rest (make it the smallest suffix)
        # After the swap, the part to the right of i is still in descending order.
        # To make the number as small as possible, reverse it to ascending order.
        l, r = i + 1, n - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1

```

## 11. Container With Most Water[[Link](https://leetcode.com/problems/container-with-most-water/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/max-water-container)]

```python
# time: O(n); space: O(1)
class Solution:
    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        res = 0

        while l < r:
            area = min(height[l], height[r]) * (r - l) 
            res = max(res, area)

            if height[l] <= height[r]:
                l += 1
            else:
                r -= 1
                    
        return res
```

## 42. Trapping Rain Water[[Link](https://leetcode.com/problems/trapping-rain-water/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/trapping-rain-water)]

```python
# two pointers
# time: O(n); space: O(1)
# hint: max_left, max_right to contains actual values 
# take the minimum of the max left height and max right height
# maximum height to the left of i (inclusive).
# maximum height to the right of i (inclusive).
class Solution:
    def trap(self, height: List[int]) -> int:
        # handle a case when no values in list (optional)
        # if not height:
        #     return 0

        l, r = 0, len(height) - 1
        max_left, max_right = height[l], height[r]

        res = 0
        while l < r:
            # the code shown below logic, take the min(l, r) - h[i]
            if max_left < max_right:
                l += 1
                max_left = max(max_left, height[l])
                res += max_left - height[l]
            else:
                r -= 1
                max_right = max(max_right, height[r])
                res += max_right - height[r]
        
        return res
"""explain
so the overal logic is min(i, j) - h[i]
in code
    min(i, j) => 
        if max_left < max_right:
            l += 1
            max_left = max(max_left, height[l])
            res += max_left - height[l] => the part find the min i or j and - h[i]
"""
```

## 2560. House Robber IV[[Link](https://leetcode.com/problems/house-robber-iv/description/)]
- video explaination[[Link](https://neetcode.io/solutions/house-robber-iv)]

```python
# searching in a range
# time: O(n log m); space: O(1)
class Solution:
    def minCapability(self, nums: List[int], k: int) -> int:
        def can_rob_with_capability(cap): # this function is to test if rob can rob one given the capacity and k
            i = 0
            count = 0
            while i < len(nums):
                if nums[i] <= cap:
                    count += 1
                    i += 2
                else:
                    i += 1
                if count == k:
                    break
            return count == k

        l, r = min(nums), max(nums) # indicates capacity range
        res = 0
        while l <= r:
            mid = l + (r - l) // 2 # try to find one possible max capacity
            if can_rob_with_capability(mid):
                res = mid
                r = mid - 1
            else:
                l = mid + 1
        
        return res
```

## 26. Remove Duplicates from Sorted Array[[Link](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/remove-duplicates-from-sorted-array)]

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        l = 1
        for r in range(1, len(nums)):
            if nums[r] != nums[r - 1]:
                nums[l] = nums[r]
                l += 1
        return l
```

## 80. Remove Duplicates from Sorted Array II[[Link](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/solutions/remove-duplicates-from-sorted-array-ii)]

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        l = 0
        for r in range(len(nums)):
            # l < 2 means we have added fewer than 2 elements
            # so there’s no way we have more than 2 duplicates yet
            if l < 2 or nums[r] != nums[l - 2]:
                nums[l] = nums[r]
                l += 1
        return l
```

## 74. Search a 2D Matrix[[Link](https://leetcode.com/problems/search-a-2d-matrix/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/search-2d-matrix)]
- hint: flatten the matix, indexing use same concept like hashing matrix[mid // cols][mid % cols]

```python
# based on
# arr = [1, 3, 3, 4, 5, 6, 7, 8]

# def binary_search(arr, tareget):
#     l, r = 0, len(arr) - 1

#     while l <= r:
#         mid = (l + r) // 2

#         if target > arr[mid]:
#             l = mid + 1
#         elif target < arr[mid]:
#             r = mid - 1
#         else:
#             return mid
#     return - 1

# time: O(log(n * m))
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        rows, cols = len(matrix), len(matrix[0])

        l, r = 0, rows * cols - 1
        while l <= r:
            mid = (r + l) // 2
            mid_val = matrix[mid // cols][mid % cols]
            
            if target > mid_val:
                l = mid + 1
            elif target < mid_val:
                r = mid - 1
            else:
                return True
        return False
```

## 374. Guess Number Higher or Lower[[Link](https://leetcode.com/problems/guess-number-higher-or-lower/description/)]
- video explaination[[Link](https://neetcode.io/problems/guess-number-higher-or-lower)]

```python
class Solution:
    def guessNumber(self, n: int) -> int:
        l, r = 1, n
        while l <= r:
            mid = (l + r) // 2
            if guess(mid) == 1:
                l = mid + 1
            elif guess(mid) == -1:
                r = mid - 1
            else:
                return mid
        return -1
```

## 153. Find Minimum in Rotated Sorted Array[[Link](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/?envType=study-plan-v2&envId=top-interview-150)]
- video explaination[[Link](https://neetcode.io/problems/find-minimum-in-rotated-sorted-array)]

```python
# never let l, r pointer to overlap
# so when break out the loop, the nums[l] will be the smallest
class Solution:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            mid = (l + r) // 2
            if nums[mid] < nums[r]:
                r = mid
            else:
                l = mid + 1
        return nums[l]
```

## *33. Search in Rotated Sorted Array[[Link](https://leetcode.com/problems/search-in-rotated-sorted-array/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/find-target-in-rotated-sorted-array)]

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = l + (r - l) // 2
            if target == nums[mid]:
                return mid
            # check which sorted portion we're in
            # left portion, determin the mid belongs to left portion or right portion
            if nums[l] <= nums[mid]:
                if target > nums[mid] or target < nums[l]: # two cases: 1. imagine a sorted array with no rotation, if target > mid val, them l = mid + 1 search right portion. 2. in rotated scinario, if target < l pointer val, this also should find right portion
                    l = mid + 1
                else:
                    r = mid - 1
            # right
            else:
                if target < nums[mid] or target > nums[r]:
                    r = mid - 1
                else:
                    l = mid + 1
        return -1
```

## 875. Koko Eating Bananas[[Link](https://leetcode.com/problems/koko-eating-bananas/description/)]

- video explaination[[Link](https://neetcode.io/problems/eating-bananas)]

```python
# time: O(n * log m); space: O(1)
# l , r poiinter record the number of banana koko may eat per hour
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l, r = 1, max(piles)
        res = r
        # k: minumum eating speed
        while l <= r:
            k = l + (r - l) // 2

            total_time = 0
            for p in piles:
                total_time += math.ceil(float(p) / k)
            # we want to find the minimun value of k, so if we find total hour(total time) is less than h, 
            # try to find one that is slowr (smaller k)
            if total_time <= h:
                res = k
                r = k - 1
            else:
                l = k + 1
        return res
```

## 981. Time Based Key-Value Store[[Link](https://leetcode.com/problems/time-based-key-value-store/description/)]

- video explaination[[Link](https://neetcode.io/problems/time-based-key-value-store)]

```python
class TimeMap:

    def __init__(self):
        self.hash_table = {} # key: list of [val, timestamp]

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.hash_table:
            self.hash_table[key] = []
        self.hash_table[key].append([value, timestamp])

    def get(self, key: str, timestamp: int) -> str:
        res = ""
        values = self.hash_table.get(key, [])

        # run binary search
        l, r = 0, len(values) - 1
        while l <= r:
            mid = l + (r - l) // 2
            if values[mid][1] <= timestamp:
                res = values[mid][0]
                l = mid + 1
            else:
                r = mid - 1
        return res


# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)
```

## *4. Median of Two Sorted Arrays[[Link](https://leetcode.com/problems/median-of-two-sorted-arrays/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/median-of-two-sorted-arrays)]

```python
# brute force way
# time: O((n + m) log(n + m)); space: O(n + m)
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        len1 = len(nums1)
        len2 = len(nums2)
        merged = nums1 + nums2
        merged.sort()
        
        totalLen = len(merged)
        if totalLen % 2 == 0:
            return (merged[totalLen // 2 - 1] + merged[totalLen // 2]) / 2.0
        else:
            return merged[totalLen // 2]

# time: O(log(min(n, m))); space: O(1)
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        a, b = nums1, nums2 # assign two arrs to a, b
        total = len(nums1) + len(nums2)
        half = total // 2

        if len(b) < len(a):
            a, b = b, a
        
        # run binary search on a
        l, r = 0, len(a) - 1
        while True:
            i = l + (r - l) // 2 # middle value of arr a
            j = half - i - 2 # middle value of arr b

            # anchor the partitions for two arrays
            a_left = a[i] if i >= 0 else float("-infinity")
            a_right = a[i + 1] if (i + 1) < len(a) else float("infinity")
            b_left = b[j] if j >= 0 else float("-infinity")
            b_right = b[j + 1] if (j + 1) < len(b) else float("infinity")

            if a_left <= b_right and b_left <= a_right:
                # odd
                if total % 2:
                    return min(a_right, b_right)
                # even
                else:
                    return (max(a_left, b_left) + min(a_right, b_right)) / 2
            elif a_left > b_right:
                r = i - 1
            else:
                l = i + 1
        return -1
```

## 1343. Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold[[Link](https://leetcode.com/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/description/)]

- video explaination[[Link](https://neetcode.io/solutions/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold)]

```python
# time: O(n); space: O(1)
class Solution:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        res = 0
        curr_sum = sum(arr[:k-1])

        for l in range(len(arr) - k + 1):
            curr_sum += arr[l + k - 1] # add value at right pointer
            if (curr_sum / k) >= threshold:
                res += 1
            curr_sum -= arr[l] # pop the window
        
        return res

class Solution:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        l, total, res = 0, 0, 0

        for r in range(len(arr)):
            total += arr[r]

            if r - l + 1 == k:
                avg = total / k
                if avg >= threshold:
                    res += 1
                total -= arr[l]
                l += 1

        return res
```

## 209. Minimum Size Subarray Sum[[Link](https://leetcode.com/problems/minimum-size-subarray-sum/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/minimum-size-subarray-sum)]

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l, total = 0, 0
        length = float("inf")

        for r in range(len(nums)):
            total += nums[r]
            while total >= target:
                length = min(length, r - l + 1)
                total -= nums[l]
                l += 1
        
       return length if length != float('inf') else 0
```

## 3. Longest Substring Without Repeating Characters[[Link](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/longest-substring-without-duplicates)]
- hint: main logic is, if the right pointer chacter is in hashset, then iterate through the window using left pointer and pop the left pointer charater when find it
```python
# time & space: O(n)
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        window = set()
        l, length = 0, 0

        for r in range(len(s)):
            while s[r] in window:
                window.remove(s[l])
                l += 1
            window.add(s[r])
            length = max(length, r - l + 1)
        return length
    
# Longest Substring with At Most Two Distinct Characters
# Medium
# Longest Substring with At Most K Distinct Characters
# Medium
# Subarrays with K Different Integers
# Hard
# Maximum Erasure Value
# Medium
# Number of Equal Count Substrings
# Medium
# Minimum Consecutive Cards to Pick Up
# Medium
# Longest Nice Subarray
# Medium
# Optimal Partition of String
# Medium
# Count Complete Subarrays in an Array
# Medium
# Find Longest Special Substring That Occurs Thrice II
# Medium
# Find Longest Special Substring That Occurs Thrice I
# Medium
```

## 159. Longest Substring with At Most Two Distinct Characters[[Link](https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/description/)]

```python
# time & space: O(n)
class Solution:
    def lengthOfLongestSubstringTwoDistinct(self, s: str) -> int:
        window = defaultdict(int) # char -> freq
        l, length = 0, 0

        for r in range(len(s)):
            window[s[r]] += 1

            while len(window) > 2:
                window[s[l]] -= 1
                if window[s[l]] == 0:
                    del window[s[l]]
                l += 1
            
            length = max(length, r - l + 1)
        
        return length

# or similar question - 340. Longest Substring with At Most K Distinct Characters
class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        l, length = 0, 0
        window = defaultdict(int)

        for r in range(len(s)):
            window[s[r]] += 1

            while len(window) > k:
                window[s[l]] -=1
                if window[s[l]] == 0:
                    del window[s[l]]
                l += 1

            length = max(length, r - l + 1)
        
        return length

```

## 424. Longest Repeating Character Replacement[[Link](https://leetcode.com/problems/longest-repeating-character-replacement/description/)]

- video explaination[[Link](https://neetcode.io/problems/longest-repeating-substring-with-replacement)]
- hint: the offset of (r - l + 1) - max(count.values()) can get the val compare to k, if less than k, shrink the window using left pointer

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        l, res = 0, 0
        count = {} # pair in character, frequency

        for r in range(len(s)):
            count[s[r]] = 1 + count.get(s[r], 0)

            while (r - l + 1) - max(count.values()) > k:
                count[s[l]] -= 1
                l += 1
            
            res = max(res, r - l + 1)
        
        return res

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        l, length = 0, 0
        count = {} # char -> freq

        for r in range(len(s)):
            count[s[r]] = 1 + count.get(s[r], 0)
            while (r - l + 1) - max(count.values()) > k:
                count[s[l]] -= 1
                l += 1
            length = max(length, (r - l + 1))

        return length
```

## 121. Best Time to Buy and Sell Stock[[Link]](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/?envType=study-plan-v2&envId=top-interview-150)

- video explaination[[Link](https://neetcode.io/problems/buy-and-sell-crypto)]
- hint: two pointers, if the value of r - l > 0, then compare, if value of r - l < 0, then reset the l = r
    - outside the conditions, the r should be iterate throught each price anyway, so r += 1

```python
# time: O(n); space: O(1)
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        l, res = 0, 0
        
        for r in range(len(prices)):
            if prices[r] > prices[l]:
                profit = prices[r] - prices[l]
                res = max(res, profit)
            else:
                l = r
        
        return res
```

## 122. Best Time to Buy and Sell Stock II[[Link](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/description/)]

```python
# the biggest diff from buy & sell stock I is:
#       multiple buy & sell
#       profit is incremented through every purchases and sell
# time: O(n); space: O(1)
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        l, res = 0, 0

        for r in range(1, len(prices)):
            if prices[r] > prices[l]:
                res += prices[r] - prices[l]
                l = r
            else:
                l = r
        
        return res
```

## 567. Permutation in String[[Link](https://leetcode.com/problems/permutation-in-string/description/)]

- video explaination[[Link](https://neetcode.io/problems/permutation-string)]
```python
# brute-force
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        s1 = sorted(s1)

        for i in range(len(s2)):
            for j in range(i, len(s2)):
                sub_str = s2[i:j + 1]
                sub_str = sorted(sub_str)
                if s1 == sub_str:
                    return True
        return False

# sliding window
# time: O(n); space: O(1)
# 1
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False
        
        s1_count, s2_count = [0] * 26, [0] * 26
        for i in range(len(s1)):
            s1_count[ord(s1[i]) - ord('a')] += 1
            s2_count[ord(s2[i]) - ord('a')] += 1
        
        # at this stage, if two are equal, immediate return
        if s1_count == s2_count:
            return True
        
        for i in range(len(s1), len(s2)):
            # sliding part: add and remove s2
            # add
            s2_count[ord(s2[i]) - ord('a')] += 1
            # remove the leftmost
            s2_count[ord(s2[i - len(s1)]) - ord('a')] -= 1
            if s1_count == s2_count:
                return True
        return False

# 2
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        s1_count, s2_count = [0] * 26, [0] * 26
        for i in range(len(s1)):
            s1_count[ord(s1[i]) - ord('a')] += 1
            s2_count[ord(s2[i]) - ord('a')] += 1
        
        matches = 0
        for i in range(26):
            matches += (1 if s1_count[i] == s2_count[i] else 0)
        
        l = 0
        for r in range(len(s1), len(s2)):
            if matches == 26:
                return True
            
            index = ord(s2[r]) - ord('a')
            s2_count[index] += 1
            if s1_count[index] == s2_count[index]:
                matches += 1
            elif s1_count[index] + 1 == s2_count[index]:
                matches -= 1

            index = ord(s2[l]) - ord('a')
            s2_count[index] -= 1
            if s1_count[index] == s2_count[index]:
                matches += 1
            elif s1_count[index] - 1 == s2_count[index]:
                matches -= 1
            l += 1
        return matches == 26
```

## 76. Minimum Window Substring[[Link](https://leetcode.com/problems/minimum-window-substring/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/minimum-window-with-characters)]

```python
# time & space: O(n)
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if t == "":
            return ""
        
        count_t, window = {}, {}
        # we need to use count_t hashmap to compare with s
        for c in t:
            count_t[c] = 1 + count_t.get(c, 0)
        
        have, need = 0, len(count_t)
        res, res_len = [-1, -1], float('inf') # one store the result pointer, one store the
        l = 0
        for r in range(len(s)):
            c = s[r]
            window[c] = 1 + window.get(c, 0)

            if c in count_t and window[c] == count_t[c]:
                have += 1
            
            while have == need:
                # update the result (record l, r pointers), r - l + 1=lenght of current window
                if (r - l + 1) < res_len:
                    res = [l, r]
                    res_len = (r - l + 1)
                # pop from the left of the window
                window[s[l]] -= 1
                if s[l] in count_t and window[s[l]] < count_t[s[l]]:
                    have -= 1
                l += 1

        l, r = res # this is the shortes length pointers
        return s[l: r + 1] if res_len != float('inf') else ""
```

## *30. Substring with Concatenation of All Words[[Link](https://leetcode.com/problems/substring-with-concatenation-of-all-words/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://leetcode.com/problems/sliding-window-maximum/description/)]

```python

```

## 239. Sliding Window Maximum[[Link](https://leetcode.com/problems/sliding-window-maximum/description/)]

- video explaination[[Link](https://neetcode.io/problems/sliding-window-maximum?list=blind75)]

```python
# brute force
# time: O(n * k); space: O(1), O(n - k + 1) for output array
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = []

        for i in range(len(nums) - k + 1):
            max_val = nums[i]
            for j in range(i, i + k):
                max_val = max(max_val, nums[j])
            res.append(max_val)

        return res


# deque
# time & space: O(n)
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = []
        q = deque()  # store indices
        l = 0

        for r in range(len(nums)):
            # Remove indices from back while nums[r] > nums[q[-1]]
            while q and nums[r] > nums[q[-1]]:
                q.pop()
            q.append(r)

            # Remove left index if it's out of the current window
            if q[0] < l:
                q.popleft()

            # Start recording results when the window reaches size k
            if r + 1 >= k:
                res.append(nums[q[0]])
                l += 1

        return res  

        # more logically make sense
        # for r in range(len(nums)):
        #     while q and nums[r] > nums[q[-1]]:
        #         q.pop()
        #     q.append(r) 

        #     if r + 1 >= k:
        #         res.append(nums[q[0]])
        #         l += 1
            
        #     if q[0] < l:
        #         q.popleft()
```