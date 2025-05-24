# Arrays

## Prefix Sum[[linnk](https://neetcode.io/courses/advanced-algorithms/4)]
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

## Two Pointers[[Link](https://neetcode.io/courses/advanced-algorithms/3)]
- Q: Check if an array is palindrome.
```python
# time: O(n)
def ifPalindrome(word):
    l, r = 0, len(word) - 1
    while l < r:
        if word[l] != word[r]:
            return False
        l += 1
        r -= 1
    return True
```

- Q: Given a sorted input array, return the two indices of two elements which sums up to the target value. Assume there's exactly one solution.
```python
# time: O(n)
def targetSum(nums, target):
    l, r = 0, len(nums) - 1
    while l < r:
        if num[l] + nums[r] > target:
            r -= 1
        elif num[l] + nums[r] < target:
            l += 1
        else:
            return [l, r]
```

## Binary Search[[Link](https://neetcode.io/courses/dsa-for-beginners/14)]

- an efficient way of searching for elements within a sorted array

```python
# time complexity: O(log n)
arr = [1, 3, 3, 4, 5, 6, 7, 8]

def binary_search(arr, tareget):
    l, r = 0, len(arr) - 1

    while l <= r:
        mid = (l + r) // 2

        if target > arr[mid]:
            l = mid + 1
        elif target < arr[mid]:
            r = mid - 1
        else:
            return mid
    return - 1
```

