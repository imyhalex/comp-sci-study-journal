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

## 1679. Max Number of K-Sum Pairs[[Link](https://leetcode.com/problems/max-number-of-k-sum-pairs/description/?envType=study-plan-v2&envId=leetcode-75)]

```python
# time: O(n log n); space: O(1)
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        nums.sort()
        l, r = 0, len(nums) -1
        res = 0

        while l < r:
            val = nums[l] + nums[r]
            if val < k:
                l += 1
            elif val > k:
                r -= 1
            else:
                l += 1
                r -= 1
                res += 1
        return res
```

## 2239. Find Closest Number to Zero[[Link](https://leetcode.com/problems/find-closest-number-to-zero/description/)]

```python
class Solution:
    def findClosestNumber(self, nums: List[int]) -> int:
        res = []
        min_dist = float('inf')
        for n in nums:
            dist = abs(n - 0)
            if dist < min_dist:
                min_dist = dist
                res = [n] # reset list with new closest number
            elif dist == min_dist:
                res.append(n)
        
        return max(res)
```

## 1838. Frequency of the Most Frequent Element[[Link](https://leetcode.com/problems/frequency-of-the-most-frequent-element/description/)]

- video explaination[[Link](https://neetcode.io/problems/frequency-of-the-most-frequent-element?list=allNC)]

```python
# time: O(n log n); space: O(1)
class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
        """
        sorting + sliding window + prefix sum
        """
        nums.sort()
        l = 0
        total, res = 0, 0

        for r in range(len(nums)):
            total += nums[r]
            
            # this is the condition where we going to have greater thatn k operations, which is invalid
            while (r - l + 1) * nums[r] - total > k:
                total -= nums[l]
                l += 1

            res = max(res, r - l + 1)
        return res
```