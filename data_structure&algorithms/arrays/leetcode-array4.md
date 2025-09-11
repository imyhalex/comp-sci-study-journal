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

## 844. Backspace String Compare[[Link](https://leetcode.com/problems/backspace-string-compare/description/)]

- video explaination[[Link](https://neetcode.io/solutions/backspace-string-compare)]

```python
# solution 1: stack
# time: O(n + m); space: o(n + m)
class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        def build(string):
            res = []
            for ch in string:
                if ch == "#":
                    if res:
                        res.pop()
                else:
                    res.append(ch)
            return res
        
        return build(s) == build(t)
    
# solution 2: two pointer
# time: O(n + m); space: O(1)
class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        """
        s = "#cb#c"
        t = "cd#c"
        """
        def get_next_valid_char_index(string, index):
            skip = 0
            while index >= 0:
                if string[index] == '#':
                    skip += 1
                elif skip > 0:
                    skip -= 1
                else:
                    break
                index -= 1
            return index
        
        i, j = len(s) - 1, len(t) - 1
        while i >= 0 or j >= 0:
            i = get_next_valid_char_index(s, i)
            j = get_next_valid_char_index(t, j)

            # Compare characters
            if i >= 0 and j >= 0:
                if s[i] != t[j]:
                    return False
            elif i >= 0 or j >= 0:
                # One is done, the other is not
                return False
            
            i -= 1
            j -= 1
        return True
```

## 🧪 Test Input:

```python
s = "#cb#c"
t = "cd#c"
```

We expect both to reduce to `"c"` → should return `True`.

### Initial Setup:

```python
i = len(s) - 1 = 4  → s[4] = 'c'
j = len(t) - 1 = 3  → t[3] = 'c'
```

---

### 🔁 1st Iteration:

#### Step 1: Apply `get_next_valid_char_index(s, i)`

```python
i = 4, s[4] = 'c'
skip = 0
→ not '#', skip == 0 → return 4
```

#### Step 2: Apply `get_next_valid_char_index(t, j)`

```python
j = 3, t[3] = 'c'
→ not '#', skip == 0 → return 3
```

#### Compare characters:

```python
s[4] == t[3] → 'c' == 'c' → ✅ OK
```

Move pointers:

```python
i -= 1 → i = 3
j -= 1 → j = 2
```

---

### 🔁 2nd Iteration:

#### Step 1: `get_next_valid_char_index(s, 3)` → s\[3] = `#`

```python
skip = 0
s[3] == '#' → skip = 1
i = 2

s[2] = 'b' → skip = 1 → skip -= 1 → skip = 0
i = 1

s[1] = 'c' → not '#' and skip == 0 → return 1
```

✅ Found `i = 1` → s\[1] = `'c'`

---

#### Step 2: `get_next_valid_char_index(t, 2)` → t\[2] = `#`

```python
skip = 0
t[2] == '#' → skip = 1
j = 1

t[1] = 'd' → skip = 1 → skip -= 1 → skip = 0
j = 0

t[0] = 'c' → not '#' and skip == 0 → return 0
```

✅ Found `j = 0` → t\[0] = `'c'`

---

#### Compare:

```python
s[1] == t[0] → 'c' == 'c' → ✅ OK
```

Move pointers:

```python
i = 0, j = -1
```

---

### 🔁 3rd Iteration:

#### `get_next_valid_char_index(s, 0)` → s\[0] = `#`

```python
skip = 0
s[0] == '#' → skip = 1
i = -1

→ End of string, return -1
```

#### `get_next_valid_char_index(t, -1)` → already -1

---

### Compare:

```python
i == -1, j == -1 → ✅ both finished
→ return True
```

---

## ✅ Summary of Logic:

| Step                        | What’s Happening                            |
| --------------------------- | ------------------------------------------- |
| `get_next_valid_char_index` | Skips backspaces and deleted characters     |
| Main while loop             | Compares next valid chars from end to start |
| `i >= 0 or j >= 0`          | Keeps going until **both strings are done** |
| `i >= 0 and j >= 0`         | Ensures we compare valid characters         |
| Final return                | True if all matched, False otherwise        |



## *1888. Minimum Number of Flips to Make the Binary String Alternating[[Link](https://leetcode.com/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/description/)]

- video explaination[[Link](https://neetcode.io/solutions/minimum-number-of-flips-to-make-the-binary-string-alternating)]

```python
# time: O(n)
```

## 2486. Append Characters to String to Make Subsequence [[Link](https://leetcode.com/problems/append-characters-to-string-to-make-subsequence/description/)]
```py
# time: O(n); space: O(1)
class Solution:
    def appendCharacters(self, s: str, t: str) -> int:
        """
        Two pointer approach:
        - i points to s
        - j points to t
        - If s[i] == t[j], move both pointers
        - Otherwise, move i only
        - When i reaches the end of s, the number of characters left in t (from j to end)
          are the ones we need to append to make t a subsequence of s.
        """
        i, j = 0, 0
        n, m = len(s), len(t)
        
        while i < n and j < m:
            if s[i] == t[j]:
                i += 1
                j += 1
            else:
                i += 1
        
        return len(t) - j
```

## 118. Pascal's Triangle[[Link](https://leetcode.com/problems/pascals-triangle/description/)]

- video explaination[[Link](https://neetcode.io/problems/pascals-triangle?list=allNC)]

```py
# tims: O(n ^ 2); space: O(n ^ 2)
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        res = [[1]]

        for i in range(numRows - 1): # n - 1 because already do one row [1] above
            tmp = [0] + res[-1] + [0]
            row = []
            for j in range(len(res[-1]) + 1):
                row.append(tmp[j] + tmp[j + 1])
            res.append(row)
        return res
```

## 929. Unique Email Addresses[[Link](https://leetcode.com/problems/unique-email-addresses/description/)]

```py
"""
Question Understanding:
    - Input a list of emails, 
        - Emails format : local_name@domain_name.com
    - Output: Interger, that count the unique number of emails under the given normalization rules
        - the local part can contain '.' and '+'
            - '.': remove it and trea the format like "a.bc" as "abc"
            - '+': ignore everything after the first '+' in the local part such as "a+bc" becomes "a"

Assumputions:
Let's assume:
    - the input list emails is not infinty, it has cap: 0 <= emails.length <= 10^4
    - each email.length <= 100
    - each eamil only contains valid ASCII characters
    - all inputs are syntactially valid emails
    - emails only conatians lowercase letters

Brute Froce Approach:
    - Compare every normalized email to all others -> O(n^2), which is slow for large n
    
My Approach : let the n = len(emails) and L = average length of emial -> time: O(n * L), space: O(n)
    - Maintatin a set to store normalized emails
    - For each emails, split the string at '@' into `local` and `domain` variable
        - local
            1. remove everything after the first '+'
            2. remove all '.'char
        - Join the normalized local and domain with '@'
        - Add it to the set
    - Ret: the size of the set
"""
class Solution:
    def numUniqueEmails(self, emails: List[str]) -> int:
        res = set()

        for e in emails:
            local, domain = e.split('@')
            local = local.split('+')[0].replace('.', '')
            normalized = local + '@' + domain
            res.add(normalized)
        return len(res)

```


## 2460. Apply Operations to an Array[[Link](https://leetcode.com/problems/apply-operations-to-an-array/description/)]

- video explaination[[Link](https://neetcode.io/solutions/apply-operations-to-an-array)]

```py
"""
Question Understanding:
- Input: A list of integers `nums`
    - For each index i (from 0 to len(nums) - 2):
        - If nums[i] == nums[i + 1]:
            - Set nums[i] = nums[i] * 2
            - Set nums[i + 1] = 0
- After processing all elements:
    - Shift all 0s in the list to the end (relative order of non-zero elements should be preserved)

- Output: Return the resulting list after these operations.

Assumptions:
- 1 <= len(nums) <= 10^5
- nums[i] is an integer in a valid range (e.g., within 32-bit signed int)
- The input list is mutable (we can modify it in-place or return a new list)

Edge Cases:
- All elements are 0
- All elements are unique (no merging)
- All elements are equal (maximum number of merges)
- Already merged result followed by zero (e.g., [2, 2, 0, 2])
- Only one element — should return as-is

Approach:
Let n = len(nums)

1. First pass — Merge equal adjacent elements:
    - Iterate from i = 0 to n - 2
    - If nums[i] == nums[i + 1]:
        - nums[i] *= 2
        - nums[i + 1] = 0

2. Second pass — Move all non-zero numbers to the front, then fill the rest with 0s:
    - Use a write pointer to shift all non-zero values forward
    - Fill the rest of the array with 0s

Time Complexity:
- O(n) for merging pass
- O(n) for shifting pass
- Total: O(n), Space: O(1) if done in-place
"""
# time: o(n); space: O(1)
class Solution:
    def applyOperations(self, nums: List[int]) -> List[int]:
        for i in range(len(nums) - 1):
            if nums[i] == nums[i + 1]:
                nums[i] *= 2
                nums[i + 1] = 0
        
        l = 0
        for i in range(len(nums)):
            if nums[i]:
                nums[i], nums[l] = nums[l], nums[i]
                l += 1
        return nums
```

## 2109. Adding Spaces to a String[[Link](https://leetcode.com/problems/adding-spaces-to-a-string/description/)]

- video explaination[[Link](https://neetcode.io/solutions/adding-spaces-to-a-string)]

```py
"""
Question Understanding:
- Input:
    - a string `s` with length n
    - a list of interger `spaces`; each value represents an index in `s`;
        - property: `spaces` follows 0 < spaces[i] <= len(s): which means stricky in increasing order
- Objective:
    - based on the index value in `space`, anchor the index within the `s`, and add space before that anchored char
- Output:
    - return a string 

Clarifying Questions:
- Can `spaces` contains duplicate indices? (Assume NO)
- Does the arr `spaces` contains invalid indices, such as indces that is out of range? (Assume no, all vallid)

Assumptions:
Can I assume:
- 0 <= s.length <= 10^5 ? (Yes)
- 0 <= spaces.length <= s.length - 1 ?
- All chars in `s` are lower case ?
- elements in `spaces` are sorted ?
- `spaces` are not emtpy? 

Brute Force Approach:
- For each index in `spaces`, perform string insertion at that position
- Problem: String insertion performs in O(n), so total time will becomes O(k * n)

Approach:
- Algo analysis: Time O(n), Space: O(n)
- Let i be the pointer over string s, starting at 0
- Let j be the pointer over spaces, also starting at 0
- Initialize res = [] to store characters and inserted spaces
- Loop:
    - While i < len(s) and j < len(spaces):
        - If i == spaces[j], this means we have reached a location where a space must be inserted before s[i]. So:
            - Append ' ' to res
            - Increment j to move to the next space position
        - Now, append s[i] to res (whether or not we inserted a space before it)
        - Increment i to move forward in the string
- After the loop:
    - If any characters are left in s (i.e., i < len(s)), we append the rest to res
- Finally, return "".join(res) as the result string.
"""
class Solution:
    def addSpaces(self, s: str, spaces: List[int]) -> str:
        i, j = 0, 0
        res = []
        n, m = len(s), len(spaces)

        while i < n and j < m:
            if i < spaces[j]:
                res.append(s[i])
                i += 1
            else:
                res.append(' ')
                j += 1
        
        if i < len(s):
            res.append(s[i:])
        
        return ''.join(res)
```

## 2161. Partition Array According to Given Pivot[[Link](https://leetcode.com/problems/partition-array-according-to-given-pivot/description/)]

- video explaination[[Link](https://neetcode.io/solutions/partition-array-according-to-given-pivot)]

```py
class Solution:
    def pivotArray(self, nums: List[int], pivot: int) -> List[int]:
        less, equal, greater = [], [], []

        for n in nums:
            if n < pivot:
                less.append(n)
            elif n > pivot:
                greater.append(n)
            else:
                equal.append(n)
        return less + equal + greater
```

## 1658. Minimum Operations to Reduce X to Zero[[link](https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/description/)]

- video explaination[[Link](https://neetcode.io/solutions/minimum-operations-to-reduce-x-to-zero)]

```py
"""
Question Undestanding:
- Given:
    - list of integer arr `nums`
    - a number `x`
- Opertions: 
    - each time can either take leftmost or rightmost element index `i`
    - perform `x - nums[i]`
- Output:
    - find the minum number of aboved mentioned operations to let `x` becomes zero
    - or: return -1 if no such pairs

Approach(Sliding Windows):

"""
class Solution:
    def minOperations(self, nums: List[int], x: int) -> int:
        target = sum(nums) - x
        curr_sum = 0
        max_window = -1

        l = 0
        for r in range(len(nums)):
            curr_sum += nums[r]

            while l <= r and curr_sum > target:
                curr_sum -= nums[l]
                l += 1

            if curr_sum == target:
                max_window = max(max_window, r - l + 1)

        return -1 if max_window == -1 else len(nums) - max_window
```

## 540. Single Element in a Sorted Array[[Link](https://leetcode.com/problems/single-element-in-a-sorted-array/description/)]

- video explaination[[Link](https://neetcode.io/solutions/single-element-in-a-sorted-array)]

```py
"""
Question Understanding:
- Input:
    - sorted interger arry
    - one element in the array appears one time
    - the rest of elements appear exactly two times
- Ouput:
    - an element appear only one time
- Constraints
    - only time O(log n) and space O(1) is acceptable

Clarifications:
- Can input array be empty?
- Can input array contains excatly one element, nums.length == 1?
- Ascending order?

Assumpution:
- 1 <= nums.length <= 10^5
- 0 <= nums[i] <= 10^5

Cases:
- nums = [1,1,2,3,3,4,4,8,8], ret = 2
- nums = [3,3,7,7,10,11,11], ret = 10
- nums = [0], ret = 0

Simple Operations:
- Binary Search
- Index parity check (even/odd index)
- Compare nums[m] with its neigbhor
- Shrink search space based on pattern of duplicaion

Approach:
- Maintain:
    - `l` ptr assign value 0, nums[0]
    - `r` ptr assign value `nums.length - 1` indicates the last element in the posision
- Steps:
    - Constrctut a loop that evaluetas `l < r`
    - Keep comupting the mid point m = l + (r - l) // 2
    - If the `m` is even
        - Check if nums=[m] == num[m + 1]
            - If true -> the unique element must be after the `m` -> l = m + 2
            - Else -> the unique element is before `m` ->  r = m
    - If the `m` is odd
        - Check of the nums[m] == nums[m - 1]
            - If true -> unique element must be after m -> l = m + 1
            - If false -> unique is nefore m -> r = m
    - When loop ends, reutrn the nums[l]
"""

class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1

        while l < r:
            m = l + (r - l) // 2

            if m % 2 == 0:
                if nums[m] == nums[m + 1]:
                    l = m + 2
                else:
                    r = m
            else:
                if nums[m] == nums[m - 1]:
                    l = m + 1
                else:
                    r = m
        return nums[l]
```

## 1498. Number of Subsequences That Satisfy the Given Sum Condition[[Link](https://leetcode.com/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/description/)]

- video explaination[[Link](https://neetcode.io/solutions/number-of-subsequences-that-satisfy-the-given-sum-condition)]

```py
"""
Question Understanding
- Input:
    - integer array `nums`
    - integr `target`
- Output:
    - a integer
    - count the number of subsequences, which
        - the sum of min and max is <= `target`
- Constraint:
    - output % 10^9 + 7

Clarification:
- Does the arr sorted such that nums[i - 1] < nums[i] < nums[i + 1] ?
- Can input arr empty?
- Can input arr contains duplicates?

Assumpution:
- 1 <= nums.length <= 10^5
- 0 <= nums[i] <= 10^5
- 0 <= target <= 10^5

Cases:
- nums = [0], target = 0 -> ret = 0
- nums = [1, 3, 3, 2], target = 3 
    -> [1], [1, 2]
    ret = 2

Simple Operations:
- Sort input array in ascending order
- Two ptrs operations (l, r)
    - one start from the first element
    - one start from the last element
- Compare the sum of two ptrs elemtent with `target`

Approach:
- Maintain:
    - `l` ptr -> l = 0
    - `r` ptr -> r = nums.length - 1
    - `res` = 0 to keep track the number of subsequences
- Steps:
    - Sort the arr -> nums.sort()
    - Precompute pow2[i] for i in [0, n]
    - Construct a loop keep evalutate l <= r
        - if nums[l] + nums[r] <= target
            - res += pow2[r - l]
            - increment `l` = l + 1
        - else
            - decrement `r` = r - 1
    - return res % 10^9 + 7 
"""

class Solution:
    def numSubseq(self, nums: List[int], target: int) -> int:
        nums.sort()
        res = 0
        MOD = 10**9 + 7
        n = len(nums)

        pow2 = [1] * (n + 1)
        for i in range(1, n + 1):
            pow2[i] = (pow2[i - 1] * 2) % MOD
        
        l, r = 0, n - 1
        while l <= r:
            if nums[l] + nums[r] <= target:
                res = (res + pow2[r - l]) % MOD
                l += 1
            else:
                r -= 1
        return res
```

## 3105. Longest Strictly Increasing or Strictly Decreasing Subarray[[Link](https://leetcode.com/problems/longest-strictly-increasing-or-strictly-decreasing-subarray/description/)]
```py
"""
Question Understanding:
- Input:
    - int arr `nums`
- Operations:
    - find subarray in either increasing or decraseing
    - record the length of each subarray
- Output:
    - int: longest length of the subarray after above mentioned operations

Cases:
- nums = [1, 3, 2, 1], ret: 2
- nums = [1], ret: 1
- nums = [1, 2, 3, 4, 5], ret: 5

Assumptions:
- 1 <= nums.length <= 50
- 1 <= nums[i] <= 50

Simple Operations:
- Compare the nums[i] with nums[i - 1]
    - nums[i] == nums[i - 1]
    - nums[i] < nums[i - 1]
    - nums[i] > nums[i - 1]
- Maintain counter for consecutive and decreasing runs
- Take maximum length seen

Approach:
- Algo Analysis: Time: O(n); Spcae: O(1)
- Maintain:
    - `inc_len`: current increasing length
    - `dec_len`: current decreasing length
    - `res` : record the maximum length have seen
- Steps:
    - Initialie inc_len = dec_len = 1, res = 1
    - Iterate i = 1 to n -1
        - If nums[i] > nums[i - 1]
            - inc_len += 1
            - dec_len = 1
        - Else if nums[i] < nums[i - 1]
            - inc_len = 1
            - dec_len += 1
        - Else: (nums[i] == nums[i - 1])
            - inc_len = 1
            - dec_len = 1
        - Finally: keep track of the most up-to-date length to `res`: res = max(res, inc_len, dec_len)
"""

class Solution:
    def longestMonotonicSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        res = 1
        inc_len, dec_len = 1, 1

        for i in range(1, n):
            if nums[i] > nums[i - 1]:
                inc_len += 1
                dec_len = 1
            elif nums[i] < nums[i - 1]:
                inc_len = 1
                dec_len += 1
            else:
                inc_len = dec_len = 1

            res = max(res, inc_len, dec_len)
        
        return res
```

## 1968. Array With Elements Not Equal to Average of Neighbors[[Link](https://leetcode.com/problems/array-with-elements-not-equal-to-average-of-neighbors/description/)]

```py
"""
Question Understanding:
- Input:
    - int arr `nums`
        - 0-indexed
        - contains distinct integers
- Operations:
    - Rearrange array in any order, as long as:
        - (nums[i - 1] + nums[i + 1]) / 2 != nums[i]
- Output:
    - int arr: any order of `nums` that meets the aboved mentioned requirements

Cases:
- nums = [1, 2, 3, 4, 5]
    - [1, 2, 4, 3, 5]
    - []

Assumptions:
- 0 <= nums[i] <= 10^5
- 3 <= nums.length <= 10^5

Underlying Simple Operations
- Sorting the array
- Picking elements from both ends (largest/smallest)
- Alternating placement to avoid middle-value conflicts
- Simple comparisons between triplets

Approach:
- Algo Analysis: Time O(n log n) (due to sorting), Space O(n)
- Clarify variables needed:
  - l = left pointer
  - r = right pointer
  - res = result array
- Maintain:
  - `nums` sorted in ascending order
  - Alternate picking from left and right
- Steps:
  - Step 1: Sort the array
    - Reasoning: Ensures smallest and largest are far apart to break "average" patterns
  - Step 2: Initialize two pointers (l=0, r=n-1)
    - Reasoning: Needed to access smallest and largest efficiently
  - Step 3: While res not full:
    - Append nums[l], then increment l
      - Reasoning: Place smallest remaining element
    - Append nums[r], then decrement r
      - Reasoning: Place largest remaining element
  - Step 4: Return res
    - Reasoning: Result guaranteed to avoid average condition since extremes are alternated
"""

class Solution:
    def rearrangeArray(self, nums: List[int]) -> List[int]:
        nums.sort()

        l, r = 0, len(nums) - 1
        res = []
        while len(res) != len(nums):
            res.append(nums[l])
            l += 1
            
            if l <= r:
                res.append(nums[r])
                r -= 1
        
        return res
```

## 2491. Divide Players Into Teams of Equal Skill[[Link](https://leetcode.com/problems/divide-players-into-teams-of-equal-skill/description/)]

```py
"""
Question Understanding:
- Input:
    - int arr `skill`
        - even length
- Opration:
    - Divide the players into n / 2 teams in size 2
    - sum of the skill of each teams are equal
    - calculate `chemistry` -> product of assigned two member in each team
- Output:
    - int: sum of `chemistry` (from all teams)
    - return -1 if no way to divide player

Assumptions:
- 2 <= skill.length <= 10^5
- 1 <= skill[i] <= 1000

Approach:
- Maintain:
    - `total` = sum of the `skill
    - `tatget` -> target skill sum per pair
    - `count` -> a hashmap for skill freq
    - res -> accumulated chemistry sum
- Logic:
    - count[s] to know if a skill is avaible
    - check for complement  `diff` = target - s
- Steps:
    - Compute the total sum
    - Compute target = total / (n / 2)
    - Feed the hashmap `count` in (num -> freq) pair
    - Iterate the `skill`
        - 
"""

class Solution:
    def dividePlayers(self, skill: List[int]) -> int:
        total = sum(skill)

        if total % (len(skill) // 2):
            return -1
        
        count = Counter(skill)
        target = total // (len(skill) // 2)
        res = 0

        for s in skill:
            if not count[s]:
                continue

            diff = target - s
            if not count[diff]:
                return -1
            
            res += s * diff
            count[s] -= 1
            count[diff] -= 1

        return res
```

## 162. Find Peak Element[[Link](https://leetcode.com/problems/find-peak-element/description/)]

```py
"""
Question Understanding:
- Input:
    - int arr `nums`
- Objective:
    - Try to find the pattern nums[i - 1] < nums[i] > nums[i + 1]
- Output:
    - retgurn any index i that safisty nums[i - 1] < nums[i] > nums[i + 1] pattern

Approach:
- Algo Analysis: Time O(log n), Space O(1)
- Clarify variables needed:
    - l = left boundary
    - r = right boundary
    - m = mid index
- Maintain:
    - l starts at 0
    - r starts at n - 1
- Steps:
    - While l < r:
        - Compute m = l + (r - l) // 2
        - Compare nums[m] with nums[m+1]
        - If nums[m] < nums[m+1]:
            - Reasoning: peak must lie on the right side because slope is rising
            - Move l = m + 1
        - Else:
            - Reasoning: peak is at m or to the left because slope is falling
            - Move r = m
    - When loop ends, l == r
    - Return l as the peak index
- Reasoning:
    - Each decision halves the search space
    - Guarantees finding a peak because slopes guarantee a peak somewhere
""" 

class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        
        while l < r:
            m = l + (r - l) // 2

            if nums[m] < nums[m + 1]:
                l = m + 1
            else:
                r = m
        return l
```

## 2300. Successful Pairs of Spells and Potions[[Link](https://leetcode.com/problems/successful-pairs-of-spells-and-potions/description/)]

```py
"""
Qustion Understanding:
- Inputs:
    - `spells`: int arr
    - `potions`: int arr
    - `success`: int
- Operations:
    - for each spells[i] * each elements in potions[j]
    - count the number of products >= `success`
- Output:
    - int arr: the count of number of successful spell and potion products

Clarfications:
- Can input `success` be 0?
- Does the input spells and potions sorted in ascending order?

Cases:
- spells = [1, 2, 3], potions = [1, 2, 3, 4], success = 5; ret -> [0, 2, 6]

Assumptions:
- 1 <= spells.length <= 10^5
- 1 <= potions.length <= 10^5
- 1 <= spells[i], potions[j] <= 10^5
- 1 <= success <= 10^5

Approach:
- Algo Analysis: Time: O(n log m + m log m), Space: O(n)
- Simple operations:
    - sort potions to ascending order
    - two ptrs l and r from start and the end of arr simultaniously
    - compute mid point m, for each spell, check spell * potions[m] >= sucess
    - append to res potions.length - l 
- Maintain:
    - l , r = 0, potions.length - 1
- Steps:
    - sort the potions
    - For each spell:
        - Binary search on potitions fo find first spell * potions[m] >= sucess
        - Compute the count = potion.length - 1
        - Store in output
"""

class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        potions.sort()
        res = []

        for spell in spells:
            l, r = 0, len(potions) - 1
            idx = len(potions)

            while l <= r:
                m = l + (r - l) // 2
                if spell * potions[m] >= success:
                    r = m - 1
                    idx = m
                else:
                    l = m + 1
            res.append(len(potions) - idx)
        return res
```

## 1800. Maximum Ascending Subarray Sum[[Link](https://leetcode.com/problems/maximum-ascending-subarray-sum/description/)]

```py
"""
Quesiton Understanding:
- Input:
    - `nums` integer arr
- Output:
    - Count the maximum possible sum of any of strticly increasing subarray in `nums`

Clarification:
- Can i assume the length of subarr > 1?
- Can I assume the nums.length > 1?

Cases:
- nums = [1], ret: 0
- nums = [10,20,30,40,50], ret: 150

Simple Operation
    - Construct a window only contains the subarr in ascending order
    - Condtion checks
        - grow the window if next element is greater than current element
        - or reset and shift windwo if the next element is less than current element

Approach:
- Algo Analysis: Time O(n), Space O(1)
- Maintain:
    - a right ptr `r` = 0: head (right end) of the window
    - `res`: keep track of the current max sum within the window; initial res = 0
- Steps:
    - Iterate `r` from 0 -> n - 1
        - increment the curr_sum += nums[r] if the nums[r] > prev
        - if the nums[r] is less than prev
            - reset the curr_sum = nums[r]
        - assign prev = nums[r]
        - keep recording the current maximun by updating res = max(res, curr_sum)
    - Return the result `res`
"""

class Solution:
    def maxAscendingSum(self, nums: List[int]) -> int:
        res = 0
        n = len(nums)
        prev, curr_sum = 0, 0

        for r in range(n):
            if nums[r] > prev:
                curr_sum += nums[r]
            else:
                curr_sum = nums[r]
            prev = nums[r]
            res = max(res, curr_sum)
        return res
```