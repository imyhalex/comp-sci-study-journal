## 125. Valid Palindrome[[Link](https://leetcode.com/problems/valid-palindrome/description/?envType=study-plan-v2&envId=top-interview-150)]
- video explaination[[Link](https://neetcode.io/problems/is-palindrome)]
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

## 680. Valid Palindrome II[[Link](https://leetcode.com/problems/valid-palindrome-ii/description/)]

- video explaination[[Link](https://neetcode.io/problems/valid-palindrome-ii?list=neetcode250)]

```python
# time: O(n); space: O(1)
class Solution:
    def validPalindrome(self, s: str) -> bool:
        def is_palindrome(l, r):
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
            return True
        
        l, r = 0, len(s) - 1
        while l < r:
            if s[l] != s[r]:
                # add one more layer for validation check, either add left or minus right
                """
                If they’re not equal, I try two options:
                    Skip the left character (s[l]) and check if the rest forms a palindrome.
                    Skip the right character (s[r]) and check that as well.
                """
                return (is_palindrome(l + 1, r) or is_palindrome(l, r - 1))
            l += 1
            r -= 1
        
        return True
```

## 1216. Valid Palindrome III[[Link](https://leetcode.com/problems/valid-palindrome-iii/description/)]

```python

```

## 1768. Merge Strings Alternately[[Link](https://leetcode.com/problems/merge-strings-alternately/description/)]

- video explaination[[Link](https://neetcode.io/problems/merge-strings-alternately?list=neetcode250)]

```python
# time: O(n + m); space: O(n + m)
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        res = []
        n, m = len(word1), len(word2)
        i, j = 0, 0
        while i < n or j < m:
            if i < n:
                res.append(word1[i])
            if j < m:
                res.append(word2[j])
            i += 1
            j += 1
        
        return "".join(res)
```

## 88. Merge Sorted Array[[Link](https://leetcode.com/problems/merge-sorted-array/description/)]

- video explaination[[Link](https://neetcode.io/problems/merge-sorted-array?list=neetcode250)]

```python
# time: O(m + n); space: O(1)
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        # merge in reverse order
        last = m + n - 1
        i, j = m - 1, n - 1
        
        while j >= 0:
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[last] = nums1[i]
                i -= 1
            else:
                nums1[last] = nums2[j]
                j -= 1

            last -= 1
"""
Merge Two Sorted Lists
Easy

Squares of a Sorted Array
Easy

Interval List Intersections
Medium

Take K of Each Character From Left and Right
Medium
"""
```

## 21. Merge Two Sorted Lists[[Link](https://leetcode.com/problems/merge-two-sorted-lists/description/)]

## 189. Rotate Array[[Link](https://leetcode.com/problems/rotate-array/description/)]

- video explaination[[Link](https://neetcode.io/problems/rotate-array?list=neetcode250)]

```python
# time: O(n); space: O(1)
# Using Reverse
# use mod: 
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        def reverse(l, r):
            while l < r:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
                r -= 1
        
        n = len(nums)
        k %= n
        reverse(0, n - 1)
        reverse(0, k - 1)
        reverse(k, n - 1)
```

## 881. Boats to Save People[[Link](https://leetcode.com/problems/boats-to-save-people/description/)]

- video explaination[[link](https://neetcode.io/problems/boats-to-save-people?list=neetcode250)]

```python
# time: O(n log n); space: O(1)
# no person has weight greater than boat's limit in this question
class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people.sort()
        res = 0
        l, r = 0, len(people) - 1

        while l <= r:
            remain = limit - people[r]
            r -= 1
            res += 1
            if l <= r and remain >= people[l]:
                l += 1

        return res
```

## 14. Longest Common Prefix[[Link](https://leetcode.com/problems/longest-common-prefix/description/)]

- video explaination[[Link](https://neetcode.io/problems/longest-common-prefix?list=neetcode250)]

```python
# time: O(n * m); space: O(1)
"""method
    pick a arbitrary string (choose the frist one in this example)
    itrete: ptr i in strs[0]:
        loop though every string in strs
            need to check the i ptr is in-bound or if the s[i] is equal to strs[0][i]
            if i == len(s) or s[i] != strs[0][i], return result immediatly 
        increment ressult by add strs[0][i] since we pick arbitrary one
    return result
"""
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        res = ""

        for i in range(len(strs[0])):
            for s in strs[1:]:
                if i == len(s) or s[i] != strs[0][i]:
                    return res

            res += strs[0][i]
        return res
```

## 27. Remove Element[[Link](https://leetcode.com/problems/remove-element/description/)]

- video explaination[[Link](https://neetcode.io/problems/remove-element?list=neetcode250)]

```python
# time: O(n); space: O(1)
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        k = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k
```

## 169. Majority Element[[Link](https://leetcode.com/problems/majority-element/description/)]

- video explaination[[Link](https://neetcode.io/problems/majority-element?list=neetcode250)]
- Boyer-Moore Voting Algorithm[[Link](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_majority_vote_algorithm)]
```python
"""
Start with no leader and zero votes (res = 0, count = 0)
Go through each number:
    If your vote count hits zero, pick the current number as your new candidate (res).
    If the current number equals your candidate, you gain a vote.
    If the current number differs, you lose a vote.
At the end, the majority element is the only one that could have survived all the cancellations.
"""
# Boyer-Moore Voting Algorithm
# time: O(n); space: O(1)
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        res, count = 0, 0

        for num in nums:
            if count == 0:
                res = num

            if res == num:
                count += 1
            else:
                count -= 1
        
        return res
```
## 229. Majority Element II[[Link](https://leetcode.com/problems/majority-element-ii/description/)]
- video explaination[[Link](https://neetcode.io/problems/majority-element-ii?list=neetcode250)]

```python
# time: O(n); space: O(1)
class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        count = defaultdict(int) # num -> freq of num
        res = []

        for n in nums:
            count[n] += 1

            if len(count) <= 2:
                continue
            
            new_count = defaultdict(int)
            for n, c in count.items():
                if c > 1:
                    new_count[n] = c - 1
            count = new_count
        
        # verification step, check the possible candidatesd after cancellation
        for n in count.keys():
            if nums.count(n) > len(nums) // 3:
                res.append(n)
        
        return res

```

## 912. Sort an Array[[Link](https://leetcode.com/problems/sort-an-array/description/)]

```python
# bubble sort - TLE
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        
        def swap(arr, l, r):
            tmp = arr[l]
            arr[l] = arr[r]
            arr[r] = tmp
        
        n = len(nums)
        while True:
            swapped = False
            for i in range(n - 1):
                if nums[i] > nums[i + 1]:
                    swap(nums, i, i + 1)
                    swapped = True
            if not swapped:
                break
            n -= 1  # Each pass bubbles the largest to the end
        
        return nums

# selection sort - TLE
# keep finding the min_idx
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        
        def swap(arr, l, r):
            tmp = arr[l]
            arr[l] = arr[r]
            arr[r] = tmp
        
        n = len(nums)
        for i in range(n - 1):
            min_idx = i

            for j in range(i + 1, n):
                if nums[j] < nums[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                swap(nums, i, min_idx)

        return nums

# insertion sort -TLE
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        n = len(nums)

        for i in range(1, n):
            key = nums[i]
            j = i - 1 # j is for prev one

            while j >= 0 and nums[j] > key:
                nums[j + 1] = nums[j]
                j -= 1
            
            nums[j + 1] = key

        return nums

# merge sort
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:

        def merge(arr, l, m, r):
            left_arr, right_arr = arr[l : m + 1], arr[m + 1 : r + 1]
            
            # merge temp arrays
            # initial indices for first and second subarray
            i, j = 0, 0
            k = l # ← This tells us where to start writing the merged elements in `arr`
            """
            Why not start at k = 0?
                Because you're only merging a subrange of the array: arr[l:r+1].
                Starting at k = 0 would overwrite unrelated parts of arr outside the merge range.
            """

            while i < len(left_arr) and j < len(right_arr):
                if left_arr[i] < right_arr[j]:
                    arr[k] = left_arr[i]
                    i += 1
                else:
                    arr[k] = right_arr[j]
                    j += 1
                k += 1
            
            while i < len(left_arr):
                arr[k] = left_arr[i]
                k += 1
                i += 1
            
            while j < len(right_arr):
                arr[k] = right_arr[j]
                k += 1
                j += 1


        def sort(arr, l, r):
            if l < r:
                m = l + (r - l) // 2

                sort(arr, l, m)
                sort(arr, m + 1, r)
                merge(arr, l, m, r)
        
        sort(nums, 0, len(nums) - 1)
        return nums
```

## 75. Sort Colors[[Link](https://leetcode.com/problems/sort-colors/description/)]
- video explaination[[Link](https://neetcode.io/problems/sort-colors?list=neetcode250)]
- Dutch national flag problem[[Link](https://en.wikipedia.org/wiki/Dutch_national_flag_problem)]
- quick sort[[Link](https://neetcode.io/courses/dsa-for-beginners/12)]

```python
# same idea from quick sort quick select

"""pseudo code
procedure three-way-partition(A : array of values, mid : value):
    i ← 0
    j ← 0
    k ← size of A - 1

    while j <= k:
        if A[j] < mid:
            swap A[i] and A[j]
            i ← i + 1
            j ← j + 1
        else if A[j] > mid:
            swap A[j] and A[k]
            k ← k - 1
        else:
            j ← j + 1
"""
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        def swap(arr, i, j):
            tmp = arr[i]
            arr[i] = arr[j]
            arr[j] = tmp
        
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                swap(nums, low, mid)
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else: # nums[mid] == 2
                swap(nums, mid, high)
                high -= 1

# a second way: merge sort or quick sort
# a quick sort problem, time: O(n log n); space: O(log n)
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:

        def swap(arr, i, j):
            tmp = arr[i]
            arr[i] = arr[j]
            arr[j] = tmp

        def partition(arr, low, high):  
            pivot = arr[high]           # use the last element as pivot

            i = low - 1                 # pointer for smaller element
            for j in range(low, high):
                if arr[j] < pivot:
                    i += 1
                    swap(arr, i, j)    # place smaller element to the left

            swap(arr, i + 1, high)      # do the final swap to swap the selected pivot to the right position
            return i + 1                # return the pivot index

        def quick_sort(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)  # partition index

                quick_sort(arr, low, pi - 1)    # sort left, pivot is not included bc already sorted into right position
                quick_sort(arr, pi + 1, high)   # sort right, pivot is not included bc already sorted into right position

        quick_sort(nums, 0, len(nums) - 1)
        return nums
"""
Test Case:
arr = [10, 5, 7, 3], pivot = 3
low = 0, high = 3

i = -1
for j in range(0, 3):  # j = 0,1,2
    if arr[j] < pivot:
        i += 1
        swap(i, j)
No arr[j] < pivot is ever true (pivot is 3, all arr[j] > 3) → i stays -1
Final step: swap(i + 1, high) → swap(0, 3) → puts pivot at index 0

✅ Correct output: [3, 5, 7, 10]
"""
```