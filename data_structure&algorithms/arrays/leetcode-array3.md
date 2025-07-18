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

## 41. First Missing Positive[[Link](https://leetcode.com/problems/first-missing-positive/description/)]

```python
# solution 1: greedy with sort
# time: O(n log n); time: O(1)
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        nums.sort()
        res = 1
        for n in nums:
            if n > 0 and res == n:
                res += 1
        return res

# solution 2: cycle sort
# time: O(n); space: O(1)
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        i = 0

        while i < n:
            if nums[i] <= 0 or nums[i] > n:
                i += 1
                continue
            
            index = nums[i] - 1
            if nums[i] != nums[index]:
                nums[i], nums[index] = nums[index], nums[i]
            else:
                i += 1
        
        for i in range(n):
            if nums[i] != i + 1: # i + 1 means actual number represent in that index position
                return i + 1
        
        return n + 1 # If all integers from 1 to n are present in the array, then the smallest missing positive is n + 1
        # case: nums = [1, 2, 3]
        # Nothing is missing in the range 1 to n, so the answer is: n + 1 = 3 + 1 = 4
```

---

## 🎯 Goal:

Given an array of numbers, like:

```python
[3, 4, -1, 1]
```

We want to **find the smallest missing positive number**, starting from **1**, in O(n) time and using **no extra space**.

---

## 🤔 What are we trying to do?

We're trying to **reorganize** the array **in-place** so that:

* The number **1** is at index `0`
* The number **2** is at index `1`
* The number **3** is at index `2`
* The number **4** is at index `3`
* And so on...

This way, we can just walk through the array and find out **which number is missing**.

---

## 🧪 Step-by-step Example

### Input:

```python
nums = [3, 4, -1, 1]
```

### Step 1: Rearrange the numbers

We loop through each number and try to **put it in the right place**.

Let’s walk through this loop:

#### First pass:

* `i = 0`: `nums[0] = 3`

  * 3 should be at index `2` → swap `nums[0]` and `nums[2]`
  * Array becomes: `[-1, 4, 3, 1]`

* `i = 0`: now `nums[0] = -1` → ignore it (negative or zero or too big)

* `i = 1`: `nums[1] = 4`

  * 4 should be at index `3` → swap `nums[1]` and `nums[3]`
  * Array becomes: `[-1, 1, 3, 4]`

* `i = 1`: now `nums[1] = 1`

  * 1 should be at index `0` → swap `nums[1]` and `nums[0]`
  * Array becomes: `[1, -1, 3, 4]`

* `i = 1`: now `nums[1] = -1` → skip

* `i = 2`: `nums[2] = 3`

  * 3 is already in the right place (index 2) → skip

* `i = 3`: `nums[3] = 4`

  * Already in the right place → skip

### Now the array looks like:

```
[1, -1, 3, 4]
```

---

### Step 2: Find the missing number

Now we go through the array:

* index 0 → has 1 ✅
* index 1 → has -1 ❌ (we expected 2 here)

So the answer is:

```python
2
```

---

## ✅ What's the trick here?

We're **reusing the array itself** like a "bucket" to store where each number should go.

Instead of sorting or using extra memory, we just:

1. Try to put each number in its correct index
2. Then look for the **first place** where the number doesn't match the index + 1

---

## ✅ Key Rules in the loop:

* Ignore numbers ≤ 0 or > n (they can't be the answer)
* Swap each number into the position it belongs (value `x` goes to index `x - 1`)
* Stop swapping if it's already in the right place or a duplicate

---

## Summary:

| Step      | What happens                                            |
| --------- | ------------------------------------------------------- |
| Rearrange | Put numbers `1...n` at their correct indices (in-place) |
| Scan      | Return the first index `i` where `nums[i] != i + 1`     |
| Edge case | If all are in place, return `n + 1`                     |

---

Let me know if you'd like a visual animation or want to walk through another example!


## 35. Search Insert Position[[Link](https://leetcode.com/problems/search-insert-position/description/)]

- video explaination[[Link](https://neetcode.io/problems/search-insert-position?list=neetcode250)]

```python
# time: O(log n); space: O(1)
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l <= r:
            m = l + (r - l) // 2
            if nums[m] == target:
                return m
            elif nums[m] < target:
                l = m + 1
            else:
                r = m - 1
        return l
```

## 69. Sqrt(x)[[Link](https://leetcode.com/problems/sqrtx/description/)]

- video explaination[[Link](https://neetcode.io/problems/sqrtx?list=neetcode250)]

```python
# time: O(log n); space: O(1)
class Solution:
    def mySqrt(self, x: int) -> int:
        l, r = 0, x
        res = 0

        while l <= r:
            m = l + (r - l) // 2

            if m * m < x:
                l = m + 1
                res = m
            elif m * m > x:
                r = m - 1
            else:
                return m
        
        return res
```

## 50. Pow(x, n)[[Link](https://leetcode.com/problems/powx-n/description/)]

- video explaination[[Link](https://neetcode.io/problems/pow-x-n?list=neetcode250)]

```python
# time: O(log n); space: O(log n)
class Solution:
    def myPow(self, x: float, n: int) -> float:
        def helper(x, n):
            if x == 0:
                return 0
            if n == 0:
                return 1

            res = helper(x, n // 2)  # compute x^(n//2)
            res = res * res # square it → (x^(n//2))^2
            return x * res if n % 2 else res # n % 2 is true when exponent is odd
        
        res = helper(x, abs(n))
        return res if n >= 0 else 1 / res # x^-n = 1/x^n
```

## 875. Koko Eating Bananas[[Link](https://leetcode.com/problems/koko-eating-bananas/description/)]

- video explaination[[Link](https://neetcode.io/problems/eating-bananas)]

```python
# time: O(n * log m); space: O(1)
# l , r poiinter record the number of banana koko may eat per hour
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l, r = 1, max(piles) # l, r means the speed koko can eat per hour
        res = r  # Worst case, she eats at max speed
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

# a more intuitive style
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l, r = 1, max(piles) 
        res = r

        def can_finish(speed):
            total_time = 0
            for p in piles:
                total_time += math.ceil(float(p) / speed)
            return total_time <= h

        while l <= r:
            k = l + (r - l) // 2
            if can_finish(k):
                res = k
                r = k - 1
            else:
                l = k + 1
        
        return res
```

## 1011. Capacity To Ship Packages Within D Days[[Link](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/description/)]

- video explaination[[Link](https://neetcode.io/problems/capacity-to-ship-packages-within-d-days?list=neetcode250)]

```python
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        l, r = max(weights), sum(weights)
        res = r

        def can_ship(capacity):
            days_needed, current_loads = 1, 0 # minumum 1 day anyway
            for w in weights:
                if current_loads + w > capacity:
                    days_needed += 1
                    current_loads = 0 # new day, empty the bag
                current_loads += w
            return days_needed <= days
        
        while l <= r:
            c = l + (r - l) // 2
            if can_ship(c):
                res = c
                r = c - 1
            else:
                l = c + 1
        
        return res
```

## 410. Split Array Largest Sum[[Link](https://leetcode.com/problems/split-array-largest-sum/description/)]

- video explaination[[Link](https://neetcode.io/problems/split-array-largest-sum?list=neetcode250)]

```python
# time: O(n log s); space: O(1)
class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        def can_split(largest):
            subarray, curr_sum = 0, 0
            for n in nums:
                curr_sum += n
                if curr_sum > largest:
                    subarray += 1
                    curr_sum = n # start in new subaray
            return subarray + 1 <= k
        
        l, r = max(nums), sum(nums)
        res = r

        while l <= r:
            m = l + (r - l) // 2
            if can_split(m):
                res = m
                r = m - 1
            else:
                l = m + 1
        
        return res
```
```python
curr_sum = n
```

means you're **starting a new subarray**, and `n` is the **first element** in that new subarray.

---

### 💡 Intuition:

In the `can_split(largest)` function, you’re trying to keep each subarray’s sum ≤ `largest`. So:

* You add elements to `curr_sum` as long as it doesn’t exceed `largest`.
* If `curr_sum > largest`, it means the current subarray is too big:

  * You **increment the subarray count** (`subarray += 1`).
  * Then, you **start a new subarray** beginning with `n` (the current number that caused the overflow):

    ```python
    curr_sum = n
    ```

### 🔁 Example:

For `nums = [7, 2, 5, 10, 8]`, say `largest = 15`:

* curr\_sum = 0
* Add 7 → curr\_sum = 7
* Add 2 → curr\_sum = 9
* Add 5 → curr\_sum = 14
* Add 10 → curr\_sum = 24 > 15 → too big:

  * subarray += 1
  * **curr\_sum = 10** (start new subarray)
* Add 8 → curr\_sum = 18 > 15 → again too big:

  * subarray += 1
  * **curr\_sum = 8**

Result: 3 subarrays.

---

Let me know if you want a dry run with a specific input.
