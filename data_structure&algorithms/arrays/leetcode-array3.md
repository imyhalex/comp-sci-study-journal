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

## 658. Find K Closest Elements[[Link](https://leetcode.com/problems/find-k-closest-elements/description/)]

- video explaination[[Link](https://neetcode.io/problems/find-k-closest-elements?list=neetcode250)]

```python
# time: O(log(n - k) + k); space: O(k)
class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        l, r = 0, len(arr) - k
        
        while l < r:
            m = l + (r - l) // 2
            # is the value of m (first value of the window) > values right outside of the window
            if x - arr[m] > arr[m + k] - x:
                l = m + 1
            else:
                r = m
        
        return arr[l: l + k]
```