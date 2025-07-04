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