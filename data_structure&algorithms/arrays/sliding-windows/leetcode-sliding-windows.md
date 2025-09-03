## 76. Minimum Window Substring[[Link](https://leetcode.com/problems/minimum-window-substring/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/minimum-window-with-characters)]

```python
# time & space: O(n)
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if t == "":
            return ""
        
        count_t, window = {}, {} # char -> count
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

## 242. Valid Anagram[[Link](https://leetcode.com/problems/valid-anagram/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/is-anagram)]
- hint: constructure two hashmaps and compare if they are equal
```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        count_s, count_t = {}, {}

        for i in range(len(s)):
            count_s[s[i]] = 1 + count_s.get(s[i], 0)
            count_t[t[i]] = 1 + count_t.get(t[i], 0)
        
        return count_s == count_t

# or
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        return sorted(s) == sorted(t)
```

## 49. *Group Anagrams[[Link](https://leetcode.com/problems/group-anagrams/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/anagram-groups)]
- hint: to store the count pattern as the key in hash table
```python
# time: O(m * n)
# spcae: O(m) extra space. O(m * n) space for the output list.
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)
        for s in strs:
            count = [0] * 26 # count pattern
            for c in s:
                count[ord(c) - ord('a')] += 1
            res[tuple(count)].append(s) # conver to tuple because list is mutable so cannot be the key
        return list(res.values())
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
```

## 438. Find All Anagrams in a String[[Link](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/)]

- video explaination[[Link](https://neetcode.io/solutions/find-all-anagrams-in-a-string)]

```python
# time: O(n + m); space: O(1) since at most 26 charaters
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        if len(p) > len(s):
            return []

        p_count, s_count = {}, {}
        for i in range(len(p)):
            p_count[p[i]] = 1 + p_count.get(p[i], 0)
            s_count[s[i]] = 1 + s_count.get(s[i], 0)
        
        res = []
        if p_count == s_count: # at this time, if two hash map equals, means start index 0 can be added
            res = [0]
        
        l = 0
        for r in range(len(p), len(s)):
            s_count[s[r]] = 1 + s_count.get(s[r], 0)
            s_count[s[l]] -= 1

            if s_count[s[l]] == 0:
                s_count.pop(s[l]) # pop the key
            l += 1

            if p_count == s_count:
                res.append(l)
        
        return res
```

## 3208. Alternating Groups II[[Link](https://leetcode.com/problems/alternating-groups-ii/description/)]

- video explaination[[Link](https://neetcode.io/solutions/alternating-groups-ii)]

```python
# time: O(n); space: O(1)
class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], k: int) -> int:
        n = len(colors)
        l = 0
        res = 0

        for r in range(1, n + k - 1):
            if colors[r % n] == colors[(r - 1) % n]:
                l = r
            if r - l + 1 > k:
                l += 1
            if r - l + 1 == k:
                res += 1

        return res
```

## 904. Fruit Into Baskets[[Link](https://leetcode.com/problems/fruit-into-baskets/description/)]

- video explaination[[Link](https://neetcode.io/solutions/fruit-into-baskets)]

```python
# time: O(n); spcae: O(1)
class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        count = defaultdict(int) # type -> freq
        l, res = 0, 0

        for r in range(len(fruits)):
            count[fruits[r]] += 1

            while len(count) > 2:
                f = fruits[l]
                count[f] -= 1
                if count[f] == 0:
                    del count[f]
                l += 1

            res = max(res, r - l + 1)
        return res
                
```

## 1456. Maximum Number of Vowels in a Substring of Given Length[[Link](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/description/)]

- video explaination[[Link](https://neetcode.io/solutions/maximum-number-of-vowels-in-a-substring-of-given-length)]

```python
# time: O(n); space: O(1)
class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        vowels = set(['a', 'e', 'i', 'o', 'u'])
        l, res = 0, 0
        curr = 0

        for r in range(len(s)):
            if s[r] in vowels:
                curr += 1

            while r - l + 1 > k:
                if s[l] in vowels:
                    curr -= 1
                l += 1

            res = max(res, curr)
        return res
```

## 1052. Grumpy Bookstore Owner[[Link](https://leetcode.com/problems/grumpy-bookstore-owner/description/)]

- video explaination[[Link](https://www.youtube.com/watch?v=pXFbNuEIn8Q)]

```python
class Solution:
    def maxSatisfied(self, customers: List[int], grumpy: List[int], minutes: int) -> int:
        """
        customers = [1,0,1,2,1,1,7,5]
        grumpy =    [0,1,0,1,0,1,0,1]
        minutes = 3
        ret = 16
        fix window size of two

        customers = [4, 10, 2, 3, 4, 5]
        grumpy =    [1, 0, 1, 0, 1, 0]
        minutes = 2
        ret = 4 + 10 + 2 + 4 = 20
        fix window size of two
        """
        l = 0
        window, max_window = 0, 0
        satisfied = 0 # maintain a base score
        n = len(customers)
        for r in range(n):
            if grumpy[r]:
                window += customers[r]
            else:
                satisfied += customers[r]

            if r - l + 1 > minutes:
                if grumpy[l]:
                    window -= customers[l]
                l += 1
            max_window = max(max_window, window)
        return satisfied + max_window
```

## 2379. Minimum Recolors to Get K Consecutive Black Blocks[[Link](https://leetcode.com/problems/minimum-recolors-to-get-k-consecutive-black-blocks/description/)]

- video explaination[[Link](https://neetcode.io/problems/minimum-recolors-to-get-k-consecutive-black-blocks?list=allNC)]

```python
# time: O(n); space: O(1)
class Solution:
    def minimumRecolors(self, blocks: str, k: int) -> int:
        n = len(blocks)
        nums, min_nums = 0, float('inf')
        l = 0
        for r in range(n):
            if blocks[r] == "W":
                nums += 1

            if r - l + 1 == k:
                min_nums = min(min_nums, nums)
                if blocks[l] == "W":
                    nums -= 1
                l += 1

        return min_nums
```

## 1984. Minimum Difference Between Highest and Lowest of K Scores[[Link](https://leetcode.com/problems/minimum-difference-between-highest-and-lowest-of-k-scores/description/)]

- video explaination[[Link](https://neetcode.io/problems/minimum-difference-between-highest-and-lowest-of-k-scores?list=allNC)]

```python
# time: O(n); space: O(1) or O(n)
class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        nums.sort()
        l = 0
        min_diff = float('inf')
        diff = 0
        
        for r in range(len(nums)):
            if r - l + 1 == k:
                diff = nums[r] - nums[l]
                min_diff = min(min_diff, diff)
                l += 1
        return min_diff
```

## 1652. Defuse the Bomb[[Link](https://leetcode.com/problems/defuse-the-bomb/description/)]

- video explaination[[Link](https://neetcode.io/solutions/defuse-the-bomb)]

```python
class Solution:
    def decrypt(self, code: List[int], k: int) -> List[int]:
        n = len(code)
        res = [0] * n

        l = 0
        curr_sum = 0
        for r in range(n + abs(k)):
            curr_sum += code[r % n]

            if r - l + 1 > abs(k):
                curr_sum -= code[l % n]
                l = (l + 1) % n
            
            if r - l + 1 == abs(k):
                if k > 0:
                    res[(l - 1) % n] = curr_sum
                elif k < 0:
                    res[(r + 1) % n] = curr_sum
        return res
```

## 1888. Minimum Number of Flips to Make the Binary String Alternating[[Link](https://leetcode.com/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/description/)]

```py
"""
Qustion Understanding:
- Input:
    - binary str `s`
- Operations:
    - remove the s[0] and append s[0] to the end of the `s`
    - flip s[i] (1 -> 0 or 0 -> 1)
- Objective:
    - make the result alternating (such as 101010)\
- Output:
    - int: min number of flips to perform

Clarifications:
- Do we need to check to validate if input is correct binary form?
- 

Edge Cases:
- s length = 1 → always alternating, answer = 0.
- s is already alternating → answer = 0.
- All characters same (e.g., "00000" or "11111") → flips needed = n/2 (rounded up).
- Very large input → solution must avoid recomputation.

Brute Force Approach:
- Generate all n rotations of `s`.
- For each rotation, compute mismatches against "0101..." and "1010...".
- Track minimum mismatch count.
- Time: O(n^2), too slow for n=10^5.
- Space: O(n) for storing rotations, or O(1) if computed on the fly.

Approach:
- Algo Analysis: Time O(n), Space O(n)
- Simple Operations:
    - Compare character with expected alternating pattern.
    - Rotate string virtually by shifting the "window".
    - Count mismatches (flips) against pattern "0101..." and "1010...".
    - Maintain a sliding window mismatch count efficiently.
- Maintain:
    - `alt1` = infinite string "010101..."
    - `alt2` = infinite string "101010..."
    - `s2` = `s + s` (double string to simulate rotations)
    - Two mismatch counts `mis1`, `mis2` for each window of size n.
- Steps:
    1. Build `s2 = s + s` → Reasoning: This allows us to check all rotations with a fixed-length sliding window.
    2. For each index i in [0, 2n):
        - Compare s2[i] with alt1[i] and alt2[i].
        - If not equal, increment mismatch counts.
    3. Once window length > n:
        - Subtract mismatch contribution from left side (i-n).
        - Reasoning: Maintain exactly n-length window mismatch count.
    4. Track min mismatch across all windows.
    5. Answer = min mismatch encountered.

Assumptions:
- 1 <= s.length <= 10^5
"""

class Solution:
    def minFlips(self, s: str) -> int:
        n = len(s)
        s2 = s + s
        alt1 = ''.join(["01"[(i % 2)] for i in range(2 * n)])
        alt2 = ''.join(["10"[(i % 2)] for i in range(2 * n)])

        res = n # maximum flips needed <= n
        diff1 = diff2 = 0
        l = 0
        for r in range(2 * n):
            if s2[r] != alt1[r]:
                diff1 += 1
            if s2[r] != alt2[r]:
                diff2 += 1
            
            if r - l + 1 > n:
                if s2[l] != alt1[l]:
                    diff1 -= 1
                if s2[l] != alt2[l]:
                    diff2 -= 1
                l += 1
            if r - l + 1 == n:
                res = min(res, diff1, diff2)
        
        return res
```

## 1208. Get Equal Substrings Within Budget[[Link](https://leetcode.com/problems/get-equal-substrings-within-budget/description/)]

```py
"""
Question Understanding:
- Input:
    - str: `s`
    - str: `t`
    - int: `maxCost`
- Operations:
    - change s to t
        - s[i] -> t[i], the cost = abs(s[i] - t[i]) by ascii value
- Output:
    - int: maximum length of substring, where the sum of the abs value substring cost change fron s to t <= maxCost
    - condition: no such substring, return 0

Clarifications:
- Does the inputs ensure s.length == t.length?
- Does the input only contains english letter in lower cases ascii chars?
- Can maxCost be 0 while s.length, t.length != 0?

Case:
- maxCost = 0 → return max length of identical substring
- s == t → full length is the answer
- Large maxCost → whole string is valid
- s and t differ completely with maxCost too small → return 0

Assumptions:
- 1 ≤ len(s) = len(t) ≤ 10^5
- Only lowercase letters
- maxCost ≥ 0

Approach:
- Algo Analysis: Time: O(n); Space: O(1)
- Simple Operations:
    - Compute char dif cost with abs(ord(s[i]) - ord(t[i]))
    - maintain running sum of costs
    - Adjust window when sum > maxCost
    - Track the max window length
- Maintain:
    - `l` = left pointer
    - `r` = right pointer
    - `curr_val` = current window cost
    - `res` = max length found
- Steps
    - Iterate r from 0 to n - 1
        - add cost abs val of s[r] - t[r]
        - Keep validating if `curr_val > maxCost`:
            - subtract cost at left pointer
            - move l forward by 1
        - compare the `res` with current window length r - l + 1 and find the maximum
    - Ret: `res`
"""
class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        l = 0
        n = len(s)
        res, curr_val = 0, 0

        for r in range(n):
            curr_val += abs(ord(s[r]) - ord(t[r]))

            while curr_val > maxCost:
                curr_val -= abs(ord(s[l]) - ord(t[l]))
                l += 1

            res = max(res, r - l + 1)
        return res
```