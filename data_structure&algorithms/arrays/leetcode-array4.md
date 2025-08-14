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

