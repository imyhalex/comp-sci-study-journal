# Backtracking Problems

## Subsets

- Explain[[Link](https://neetcode.io/courses/advanced-algorithms/11)]
- Time: O(n * 2^n), Space O(n)

### Distinct Element Subset
```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        subsets, currset = [], []
        self.get_subsets(0, nums, subsets, currset)
        return subsets
    
    def get_subsets(self, idx, nums, sub, curr):
        if idx >= len(nums):
            sub.append(curr.copy())
            return

        curr.append(nums[idx])
        self.get_subsets(idx + 1, nums, sub, curr)
        curr.pop()
        self.get_subsets(idx + 1, nums, sub, curr)
```

### Subsets - non-distinct elements
```python
class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        subsets, currset = [], []
        self.get_subsets(0, nums, subsets, currset)
        return subsets
    
    def get_subsets(self, idx, nums, sub, curr):
        if idx >= len(nums):
            sub.append(curr.copy())
            return

        curr.append(nums[idx])
        self.get_subsets(idx + 1, nums, sub, curr)
        curr.pop()

        while idx + 1 < len(nums) and nums[idx] == nums[idx + 1]:
            idx += 1
        self.get_subsets(idx + 1, nums, sub, curr)
```

## Combination[[Link](https://neetcode.io/courses/advanced-algorithms/12)]
- Time Complexity: O(k * 2^n)

### 1. Trivial Approach
```python
def combination(n, k):
    combs, curr = [], []
    get_combs(1, curr, combs, n, k)
    return combs

def get_combs(i, curr, combs, n, k):
    if len(curr) == k:
        combs.append(curr.copy())
        return
    if i > n:
        return
    
    curr.appen(i)
    get_combs(i + 1, curr, combs, n, k)
    curr.pop()

    get_combs(i + 1, curr, combs, n, k)
```

### 2. Optimized Approcah
- Time Complexity: O(k * C(n, k))
```python
def combination(n, k):
    combs, curr = [], []
    get_combs(1, curr, combs, n, k)
    return combs

def get_combs(i, curr, combs, n, k):
    if len(curr) == k:
        combs.append(curr.copy())
        return
    if i > n:
        return
    
    for j in range(i, n + 1):
        curr.append(j)
        get_combs(j + 1, curr, combs, n, k)
        curr.pop()
```

## Permutations[[Link](https://neetcode.io/courses/advanced-algorithms/13)]
- Time Complexity: O(n * n!)

### Recursive
```python
def permutations(nums):
    return permutations_helper(0, nums)

def permutations_helper(i, nums):
    if i == len(nums):
        return [[]]
    
    res = []
    perms = permutations_helper(i + 1, nums)
    for p in perms:
        for j in range(len(p) + 1):
            p_copy = p.copy()
            p_copy.insert(j, nums[i])
            res.append(p_copy)
    
    return res
```

```text
The recursive solution is essentially the same as the iterative one in terms of time complexity. While both are bounded below by O(n·n!) due to the size 
of the output, the practical work including list copying makes the complexity closer to O(n²·n!) in the worst-case scenario. So yes, they have 
essentially the same time complexity characteristics.
```
### Iterative
- Time Complexity: O(n^2 * n!)

```python
def permutation(nums):
    perms = [[]]

    for n in nums:
        next_perms = []
        for p in perms:
            for i in range(len(p) + 1):
                p_copy = p.copy()
                p_copy.insert(i, n)
                next_perms.append(p_copy)
        perms = next_perms
    return perms
```

## Some LC Problems
### 77. Combinations[[Link](https://leetcode.com/problems/combinations/description/)]
```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        combs, curr = [], []
        self.get_combs(1, curr, combs, n, k)
        return combs
    
    def get_combs(self, i, curr, combs, n, k):
        if len(curr) == k:
            combs.append(curr.copy())
            return 
        if i > n:
            return 
        
        for j in range(i, n + 1):
            curr.append(j)
            self.get_combs(j + 1, curr, combs, n, k)
            curr.pop()
```

### Combination Sum[[Link](https://neetcode.io/problems/combination-target-sum)]

- hint: need a variable `total` to be passed in dfs(i, total) and initialized be 0
```python
class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        combs, curr = [], []
        self.get_combs_sum(0, curr, combs, nums, target, 0)
        return combs
    
    def get_combs_sum(self, i, curr, combs, nums, target, total):
        if total == target:
            combs.append(curr.copy())
            return 
        if i >= len(nums) or total > target:
            return
        
        curr.append(nums[i])
        self.get_combs_sum(i, curr, combs, nums, target, nums[i] + total)
        curr.pop()

        self.get_combs_sum(i + 1, curr, combs, nums, target, total)

# in nested function style:
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        combs, curr = [], []

        def dfs(i, total):
            if total == target:
                combs.append(curr.copy())
                return
            
            if i >= len(candidates) or total > target:
                return
            
            curr.append(candidates[i])
            dfs(i, candidates[i] + total)
            curr.pop()

            dfs(i + 1, total)

        dfs(0, 0)
        return combs
```

### 40. Combination Sum II[[Link](https://leetcode.com/problems/combination-sum-ii/description/)]

- video explaination[[Link](https://neetcode.io/problems/combination-target-sum-ii?list=neetcode150)]

```python
# time: O(n * 2^n); space: O(n)
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        combs, curr = [], []

        def dfs(i, total):
            if total == target:
                combs.append(curr.copy())
                return
            
            if i >= len(candidates) or total > target:
                return
            
            curr.append(candidates[i])
            dfs(i + 1, candidates[i] + total)
            curr.pop()

            while i + 1 < len(candidates) and candidates[i] == candidates[i + 1]:
                i += 1
            dfs(i + 1, total)

        dfs(0, 0)
        return combs
```

### 17. Letter Combinations of a Phone Number[[Link](https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/?envType=study-plan-v2&envId=top-interview-150)]

```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        # construct a hash tablb
        table = {
            str(k): v 
            for k, v in zip(range(2, 10), ["abc", "def", "ghi", "jkl", "mno", "qprs", "tuv", "wxyz"])
        }
        combs, curr = [], ""
        self.get_letter_combs(0, curr, combs, digits, table)
        return combs
    
    def get_letter_combs(self, i, curr, combs, digits, table):
        if len(curr) == len(digits):
            combs.append(curr)
            return
        
        for letter in table[digits[i]]:
            self.get_letter_combs(i + 1, curr + letter, combs, digits, table)
```

### 46. Permutations[[Link](https://leetcode.com/problems/permutations/description/?envType=study-plan-v2&envId=top-interview-150)]
```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        return self.perms_helper(0, nums)
    
    def perms_helper(self, i, nums):
        if i == len(nums):
            return [[]]
        
        res = []
        perms = self.perms_helper(i + 1, nums)
        for p in perms:
            for j in range(len(p) + 1):
                p_copy = p.copy()
                p_copy.insert(j, nums[i])
                res.append(p_copy)
        return res

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        
        def dfs(i):
            if i == len(nums):
                return [[]]
            
            res = []
            perms = dfs(i + 1)
            for p in perms:
                for j in range(len(p) + 1):
                    p_copy = p.copy()
                    p_copy.insert(j, nums[i])
                    res.append(p_copy)
            return res
        
        return dfs(0)
```

### *47. Permutations II[[Link](https://leetcode.com/problems/permutations-ii/description/)]
- vids explaination[[Link](https://neetcode.io/solutions/permutations-ii)]
```python
# Time & Space: O(n * n!)
class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = []
        visited = [False] * len(nums)
        self.perms_helper(nums, visited, [], res)
        return res
    
    def perms_helper(self, nums, visited, path, res):
        if len(path) == len(nums):
            res.append(path.copy())
            return
        
        for i in range(len(nums)):
            # Skip elements that have already been used in the current permutation.
            if visited[i]:
                continue
            # If the current element is the same as the previous element, and the previous
            # element hasn't been used in this recursion branch, skip to avoid duplicates.
            if i > 0 and nums[i] == nums[i - 1] and not visited[i - 1]:
                continue
            # Mark the current element as used and add it to the path.
            visited[i] = True
            path.append(nums[i])
            self.perms_helper(nums, visited, path, res)
            # Remove the current element from the path and mark it as unused before the next iteration.
            path.pop()
            visited[i] = False

# Less parameters to pass if in nested function
class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = []
        visited = [False] * len(nums)

        def dfs(path):
            if len(path) == len(nums):
                res.append(path.copy())
                return

            for i in range(len(nums)):
                if visited[i]:
                    continue
                if i > 0 and nums[i] == nums[i - 1] and not visited[i - 1]:
                    continue

                visited[i] = True
                path.append(nums[i])
                dfs(path)
                path.pop()
                visited[i] = False

        dfs([])
        return res
```

## 1079. Letter Tile Possibilities[[Link](https://leetcode.com/problems/letter-tile-possibilities/description/)]

- video explaination[[Link](https://neetcode.io/solutions/letter-tile-possibilities)]

```python
# time: O(2^n)
class Solution:
    def numTilePossibilities(self, tiles: str) -> int:
        count = Counter(tiles) # char -> avaible count

        def dfs():
            res = 0
            
            for c in count:
                if count[c] > 0:
                    count[c] -= 1
                    res += 1
                    res += dfs()
                    count[c] += 1
            return res
            
        return dfs()

# or 
class Solution:
    def numTilePossibilities(self, tiles: str) -> int:
        tiles = sorted(tiles)
        used = [False] * len(tiles)
        self.count = 0

        def dfs(path):
            for i in range(len(tiles)):
                if used[i]:
                    continue
                # skips over duplicate choices on the same recursive level.
                # and previous not used in this path
                if i > 0 and tiles[i] == tiles[i - 1] and not used[i - 1]:
                    continue

                used[i] = True
                self.count += 1
                dfs(path + tiles[i])
                used[i] = False
        
        dfs("")
        return self.count
```

### *79. Word Search[[Link](https://leetcode.com/problems/word-search/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://www.youtube.com/watch?v=pfiQ_PS1g8E&t=18s)]
- hint: recursion on all four directions

```python
# time complexity: O(n * m * dfs-> 4^len(word)) -> O(n * m * 4^n)
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])
        path = set() 

        def dfs(r, c, i):
            if i == len(word):
                return True
            
            if (r < 0 or c < 0 or r >= rows or c >= cols
                or word[i] != board[r][c] or (r, c) in path):
                return False

            
            path.add((r, c))
            res = (
                dfs(r + 1, c, i + 1) or
                dfs(r - 1, c, i + 1) or
                dfs(r, c + 1, i + 1) or
                dfs(r, c - 1, i + 1)
            )
            path.remove((r, c))
            return res
        
        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False
```

### 22. Generate Parentheses[[Link](https://leetcode.com/problems/generate-parentheses/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/generate-parentheses)]
- hint: divide the dfs into recusively do open parentheses and close parentheses

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        combs, curr = [], []

        def dfs(opn_n, cls_n):
            if opn_n == cls_n == n:
                combs.append("".join(curr))
                return
            
            if opn_n < n:
                curr.append('(')
                dfs(opn_n + 1, cls_n)
                curr.pop()
            if cls_n < opn_n:
                curr.append(')')
                dfs(opn_n, cls_n + 1)
                curr.pop()
        dfs(0, 0)
        return combs 
```

### 131. Palindrome Partitioning[[Link](https://leetcode.com/problems/palindrome-partitioning/description/)]

- video explaination[[Link](https://neetcode.io/problems/palindrome-partitioning?list=neetcode150)]

```python
# time: O(n * 2^n); space: O(n) extra space, O(n * 2^n) for the output list
class Solution:
    def _is_palindrome(self, s, l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True

    def partition(self, s: str) -> List[List[str]]:
        res, curr = [], []

        def dfs(i):
            if i >= len(s):
                res.append(curr.copy())
                return
            
            for j in range(i, len(s)):
                if self._is_palindrome(s, i, j):
                    curr.append(s[i: j + 1])
                    dfs(j + 1)
                    curr.pop()
            
        dfs(0)
        return res
```

### 51. N-Queens[[Link](https://leetcode.com/problems/n-queens/description/)]

- video explaination[[Link](https://neetcode.io/problems/n-queens?list=neetcode150)]

```python
# time: O(n!); time: O(n^2)
class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        col = set()
        negative_diag = set() # -> (r - c)
        positive_diag = set() # -> (r + c)

        res = []
        grid = [["."] * n for _ in range(n)]

        def dfs(r):
            if r == n:
                copy = ["".join(row) for row in grid]
                res.append(copy)
                return

            for c in range(n):
                if c in col or (r - c) in negative_diag or (r + c) in positive_diag:
                    continue
                
                col.add(c)
                negative_diag.add(r - c)
                positive_diag.add(r + c)
                grid[r][c] = "Q"

                dfs(r + 1)
                
                # do the cleanup for the next iteration of the loop
                col.remove(c)
                negative_diag.remove(r - c)
                positive_diag.remove(r + c)
                grid[r][c] = "."
        
        dfs(0)
        return res
```

### 52. N-Queens II[[Link](https://leetcode.com/problems/n-queens-ii/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/n-queens?list=neetcode150)]

```python
# time: O(n!); time: O(n^2)
class Solution:
    def totalNQueens(self, n: int) -> int:
        col = set()
        neg_diag = set()
        pos_diag = set()
        
        self.res = 0
        def dfs(r):
            if r == n:
                self.res += 1
                return
            
            for c in range(n):
                if c in col or (r + c) in pos_diag or (r - c) in neg_diag:
                    continue
                
                col.add(c)
                neg_diag.add(r - c)
                pos_diag.add(r + c)

                dfs(r + 1)

                col.remove(c)
                neg_diag.remove(r - c)
                pos_diag.remove(r + c)

        dfs(0)
        return self.res
```

## *2707. Extra Characters in a String[[Link](https://leetcode.com/problems/extra-characters-in-a-string/description/)]

- video explaination[[Link](https://neetcode.io/problems/extra-characters-in-a-string?list=neetcode250)]

```python
# time: O(n ^ 3 + m * K); space: O(m + m * k)
class Solution:
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        words = set(dictionary)
        dp = {}

        def dfs(i):
            if i == len(s):
                return 0
            if i in dp:
                return dp[i]

            # res = 1 + dfs(i + 1) # skip curr char + initial value
            res = 1 + dfs(i + 1)
            for j in range(i, len(s)):
                if s[i: j + 1] in words:
                    res = min(res, dfs(j + 1))
            dp[i] = res # store result in cache
            return res
        
        return dfs(0)
```

## 473. Matchsticks to Square[[Link](https://leetcode.com /problems/matchsticks-to-square/description/)]

- video explaination[[Link](https://neetcode.io/problems/matchsticks-to-square?list=neetcode250)]

```python
# time: O(4 ^ n); space: O(n)
class Solution:
    def makesquare(self, matchsticks: List[int]) -> bool:
        if sum(matchsticks) % 4 != 0:
            return False
        
        length = sum(matchsticks) // 4
        sides = [0] * 4
        matchsticks.sort(reverse=True) # optimized trick

        def dfs(i):
            if i == len(matchsticks):
                return True
            
            for j in range(4):
                if sides[j] + matchsticks[i] <= length:
                    sides[j] += matchsticks[i]
                    if dfs(i + 1):
                        return True
                    # backtrack decision, like else (becasue the condition dfs(i + 1) is not true)
                    sides[j] -= matchsticks[i]
            return False
        
        return dfs(0)
```

## 1863. Sum of All Subset XOR Totals[[Link](https://leetcode.com/problems/sum-of-all-subset-xor-totals/description/)]

- video explaination[[Link](https://neetcode.io/problems/sum-of-all-subset-xor-totals?list=neetcode250)]

```python
# time: O(2 ^ n); space: O(n)
class Solution:
    def subsetXORSum(self, nums: List[int]) -> int:
        
        def dfs(i, total):
            if i == len(nums):
                return total
            
            return dfs(i + 1, total ^ nums[i]) + dfs(i + 1, total)
        
        return dfs(0, 0)
```

## 698. Partition to K Equal Sum Subsets[[Link](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/description/)]

- video explaination[[Link](https://neetcode.io/problems/partition-to-k-equal-sum-subsets?list=neetcode250)]

```python
# time: O(k * 2 ^ n); space: O(n)
class Solution:
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        if sum(nums) % k != 0:
            return False
        
        target = sum(nums) // k
        used = [False] * len(nums)
        nums.sort(reverse=True)

        def dfs(i, k, sub_sum):
            if k == 0:
                return True
            
            if sub_sum == target:
                return dfs(0, k - 1, 0) # reset the i to 0
            
            for j in range(i, len(nums)):
                if used[j] or nums[j] + sub_sum > target:
                    continue
                
                used[j] = True
                if dfs(j + 1, k, sub_sum + nums[j]): 
                    return True
                used[j] = False

                # if sub_sum == 0: # add this for pruning
                #     return False
            return False
        
        return dfs(0, k, 0)
```

## *93. Restore IP Addresses[[Link](https://leetcode.com/problems/restore-ip-addresses/description/)]

- video explaination[[Link](https://neetcode.io/solutions/restore-ip-addresses)]

```py
"""
Question Understanding:
- Input: 
    - a string `s` contains only digits
- Operations:
    - Add '.' to between the digits in `s` to make it valid IP address
    - Valid IP format:
        - Max : `255.255.255.255
        - Min : `0.0.0.0
        - all combinations between Min and Max are valid
- Ouput:
    - a list of all possible valid IP addresses
    - combination of IP address based on above mentioned operations

Clarifications:
- Can the input s.length > MAX.length where MAX is 255255255255?

Assumpution:
- 1 <= s.length <= 20
- `s` consist of digits only

Approach (Brute Force Backtracking):
- Algo analysis: Time: O(3^4); Space: O(n * m)
- Since as valid ip address is exactly 4 segment, we are try to insert 3 dots to dvide an ip address into 4 valid parts
- Case immedietaly return: s.length > 12, means input `s` is too long to be a valid ip address
- Construct a DFS/Backtracking method to explore all possible segements
    - Maintain:
        - A ptr `i` that anchor the current index of `s`
        - a variable `dots` to keep track of number '.' we have inserted
        - a `curr_ip`: str, to represent the partial ip address we have built so far
    - Base case
        - dots == 4 and i == s.length -> append the `curr_ip[:-1]` into result; ret
        - dots > 4 -> ret, not a valid combinations
    - Actual recursive step
        - try taking next 3 chars as a segment (s[i : j + 1])
        - check validity 
            - segment <= 255
            - segement does not contains any leading '0' unless segment == '0'
        - if a above mentioned validity check conditions are both satsified, recrsive call the updated `j + 1` index, `dots + 1`, and `curr_ip + segment (s[i : j + 1]) + '.'`
    - return the finaly result

"""

class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        res = []

        if len(s) > 12:
            # immediatly return empty res
            return res
        
        def dfs(i, dots, curr_ip):
            if dots == 4 and i == len(s):
                res.append(curr_ip[:-1])
                return 
            
            if dots > 4:
                return
            
            for j in range(i, min(i + 3, len(s))):
                if int(s[i : j + 1]) < 256 and (i == j or int(s[i]) != 0):
                    dfs(j + 1, dots + 1, curr_ip + s[i : j + 1] + '.')
        
        dfs(0, 0, "")
        return res
```

## 1415. The k-th Lexicographical String of All Happy Strings of Length n[[Link](https://leetcode.com/problems/the-k-th-lexicographical-string-of-all-happy-strings-of-length-n/description/)]

```py
"""
Problem Understanding
- We need to generate the k-th lexicographical "happy string" of length n.
- A happy string:
  - Characters from {‘a’, ‘b’, ‘c’}
  - No two adjacent characters are the same.
- Input:
  - n: length of the string (1 ≤ n ≤ 10)
  - k: the rank in lexicographical order (1 ≤ k ≤ 100)
- Output:
  - The k-th happy string or empty string if fewer than k exist.

Clarifying Questions
- Are we guaranteed that k is always valid? (No, if k exceeds the number of happy strings, return "")
- Should lexicographical order follow standard ASCII order (‘a’ < ‘b’ < ‘c’)? (Yes)
- Is n small enough to allow backtracking generation? (Yes, max n = 10)

Assumptuion:
- 1 <= n <= 10
- 1 <= k <= 100

Approach:
- Algo Analysis: Time O(2^n), Space O(n) recursion stack.
- Instead of sorting all, generate in lex order directly with DFS.
- Clarify variables needed:
  - result_counter: to track number of happy strings generated so far.
  - answer: to store k-th string.
  - path: current building string during recursion.
- Maintain:
  - path (string or list)
  - count (global or nonlocal variable)
  - answer (result once found)
- Steps:
  1. Start DFS with empty path.
     - Reasoning: Build string character by character.
  2. At each step, try adding 'a', 'b', 'c' in order if not equal to last character.
     - Reasoning: Avoid consecutive duplicates.
  3. When path length == n, increment counter.
     - Reasoning: Found one valid happy string.
  4. If counter == k, store answer and stop recursion.
     - Reasoning: We only care about the k-th string.
  5. If finished recursion without reaching k, return "".
     - Reasoning: Fewer than k happy strings exist.
"""

class Solution:
    def getHappyString(self, n: int, k: int) -> str:
        self.count = 0
        self.answer = ""

        def dfs(path):
            if len(path) == n:
                self.count += 1
                if self.count == k:
                    self.answer = ''.join(path)
                return

            for ch in ['a', 'b', 'c']:
                if path and path[-1] == ch:
                    continue
                if not self.answer:
                    dfs(path + [ch])
        dfs([])
        return self.answer
```

## *1849. Splitting a String Into Descending Consecutive Values[[Link](https://leetcode.com/problems/splitting-a-string-into-descending-consecutive-values/description/)]

```py
"""
Question Understanding:
- Input:
    - `s`: str contains only digit
- Oprations:
    - split `s` to let each substring in descending order and substrs[i] - substrs[i + 1] = 1
- Output:
    - bool, return true if splitted result can form a descending order else return false

Clarifications:
- Do we require at least 2 substrings? (Yes, must split into ≥ 2 parts).

Assumptions
- 1 <= s.length <= 20
- s only consists of digits
- At least two substrs required

Genral Ideas:
- a backtracking to try every possibilities for every digits
- questions to solve:
    - what is the decision tree looks like
    - what is the base case
    - what parameter is need for recursive call

Approach:
- Algo Analysis: Time ~O(2^n), Space O(n)
- Use DFS backtracking with pruning.
- Clarify variables needed:
  - prev: last used number (integer).
  - index: current position in string.
  - count: number of substrings used.
- Maintain:
  - Recursion state (index, prev, count).
- Steps:
  1. Start DFS from index=0, no prev value yet.
     - Reasoning: We must build first number arbitrarily.
  2. At each step, try every possible substring s[index:i].
     - Reasoning: Generate candidate number.
  3. If no prev, accept as first number and continue.
     - Reasoning: First number sets starting point.
  4. Else, check:
     - If candidate == prev - 1, continue recursion.
     - Reasoning: Must descend by exactly 1.
     - If > prev, skip (invalid).
  5. If index reaches len(s) and count ≥ 2, return True.
     - Reasoning: Entire string used and valid sequence.
  6. If recursion finishes without success, return False.
"""

class Solution:
    def splitString(self, s: str) -> bool:
        n = len(s)

        def dfs(index, prev, count):
            if index == n:
                return count >= 2

            num = 0
            for i in range(index, n):
                num = num * 10 + int(s[i])
                if prev is None or num == prev - 1:
                    if dfs(i + 1, num, count + 1):
                        return True
                elif prev is not None and num >= prev:
                    break
            return False
        
        return dfs(0, None, 0)
```

## 1980. Find Unique Binary String[[Link](https://leetcode.com/problems/find-unique-binary-string/description/)]

```py
"""
Question Understanding:
- Input:
    - `num`: string arr, length in `n`, each nums[i] is unique binary str
- Output:
    - a binary str in length `n` that does not appear in `num`

Assumption:
- 1 <= n <= 10
- n == nums.length
- Guaranteed to be at least one binary string is missing

Cases:
- nums = ["01", "10"]

General Idea:
- build a hash table for current exisited binaries
- backtrack every possible outcome with recursive call
- constrtuct a decision tree with depth n
    - branch 1: 0 -> 0 , 1 
    - branch 2: 1 -> 0, 1
    - each path is a possible binary
- questions to solve:
    - how to define the base case
        - if the curent recorded result length == n and it is not appear in hashtable, then return this string
    - what values need to be keep tracking of, what paramter is need for recursive call
        - path: str -> keep track of path string
    - under what condition should do recursive call

Approach:
- Algo Analysis: Time O(2^n), Space O(n)
- Maintain:
    - `seen`: a set of nums for O(1) lookup
    - recursive buider string `path`
- Steps:
    - Build set `seen` from nums
    - Defin a recursive fucntion `dfs(path)`
    - Based case: if len(path) == n
        - If path not in `seen` -> return path
        - else return None
    - Recursive call:
        - try add '0' -> dfs(path + '0')
        - if returns valid string, propagate upward
        - else try add '1'
    - return the first found valid `path`
"""
class Solution:
    def findDifferentBinaryString(self, nums: List[str]) -> str:
        n = len(nums)
        seen = set(nums)

        def dfs(path):
            if len(path) == n:
                if path not in seen:
                    return path
                return None
            
            res = dfs(path + '0')
            if res:
                return res
            
            return dfs(path + '1')
        
        return dfs("")
```

## 1593. Split a String Into the Max Number of Unique Substrings[[Link](https://leetcode.com/problems/split-a-string-into-the-max-number-of-unique-substrings/description/)]

```py
"""
Question Understanding
- Input:
    - `s`: string
- Output:
    - maximum nums of splits from `s`, each splited substr should be unique

Assumption:
- 1 <= s.length <= 10
- each s[i] contains only valid ascii value enligsh lowecase letter

Genral Idea:
- Bactrack every possible splits with recursvie call
- Record the substr as "seen" into a hashtable along with oprations
- Quetions to solve:
    - What is decision tree looks like (take first example)
        - branch 1: choose 'a' -> b, ba, bab ... -> ...
        - branch 2: choose 'ab' -> a, ab(existed), abc, abcc -> ...
        - branch 3: choose 'aba'
        - branch 4: choose "abab"
        - ....
    - What is the base case for recursive call
        - return 0 if current index == s.lenghth -> no more substr to split
    - What values need to be recorded, include
        - Parameters for recursive call
            - `i`: index for current start index in `s` to split
        - Final result
            - `count`: keep record the unique substr
    - What conditions should do recursiva call
        - pick s[i : j] (j is from i + 1 to n)
        - add it to hashtable
        - recursive call start from j
        - remove it from hashtable (backtrack)

Approach:
- Algo Analysis: Time O(2 ^ n) Space O(n)
- Maintain:
    - `seen`: a set() act like lookup table in O(1) lookup
    - `i`: curent position in a string
    - `max_count`: global tracker for maximum splits
- Steps:
    - Define recursive function dfs(i)
        - if i == len(s) -> return 0 (no more splits)
        - Iterate j in [i + 1, n]
            - substr = s[i : j]
            - if substr not in hashtable
                - add substr seen.add(substr)
                - recursive call count = 1 + dfs(j)
                - keep track max count max_count = max(max_count, count)
                - remove substr away from hashtable seen.remove(substr)
        - Return the max_count
    - Call the dfs(0)
"""
 
class Solution:
    def maxUniqueSplit(self, s: str) -> int:
        seen = set()
        n = len(s)

        def dfs(i):
            if i == len(s):
                return 0
            
            max_count = 0
            for j in range(i + 1, n + 1):
                substr = s[i : j]
                if substr not in seen:
                    seen.add(substr)
                    count = 1 + dfs(j)
                    max_count = max(max_count, count)
                    seen.remove(substr)
            return max_count
        return dfs(0)
```

## 1239. Maximum Length of a Concatenated String with Unique Characters[[Link](https://leetcode.com/problems/maximum-length-of-a-concatenated-string-with-unique-characters/description/)]

```py
"""
Question Understanding:
- Input:
    - `arr`: string array, each arr[i] concatenates with each other form a `s`
        - `s` should contains no duplicated chars
- Ouput:
    - record the length of the possible `s` and return the maximum length from those possibilities

Cases:
- arr = ["un", "iq", "ue"], ret:
    - un
    - iq
    - ue
    - uniq 
    - ique
    - unue(not possible)
    - unique(not possible)

Assumptions:
- 1 <= arr[i].length <= 20
- 1 <= arr.length <= 20
- each arr[i] contains only valid ascii value english letter in lower cases

General Ideas
- Backtrack every possible outcome with recursive calls
- record each char in arr[i] as "seen" while doing the oprations
- Questions to solve:
    - What is the decision tree look like (take first example as an example)
    - What is the base case for recursive call
    - What is the condition to do the recursive call
    - What are values and paramters to keep track of

Approach:
- Algo Analysis: Time: O(2^n * k), Space: O(n + k)
- Maintain:
  - index pointer for backtracking
  - current set of used characters
  - current length
- Steps:
  1. Pre-filter: skip arr[i] if it contains duplicates within itself
     - Reasoning: It can never contribute to valid result
  2. Define recursive dfs(index, usedChars, currLength)
     - Reasoning: systematically explore include/exclude choices
  3. Base case: if index == len(arr), return currLength
     - Reasoning: reached end of subsequence choices
  4. For each arr[index]:
     - Exclude branch → dfs(index+1, usedChars, currLength)
       - Reasoning: skipping this string might avoid conflicts
     - Include branch (only if arr[index] has no overlap with usedChars)
       - Add its chars, increase length
       - dfs(index+1, newUsedChars, currLength + len(arr[index]))
       - Reasoning: explore path where we include it
  5. Return max of two branches
     - Reasoning: ensures we pick best length across all choices
"""

class Solution:
    def maxLength(self, arr: List[str]) -> int:
        filtered = []
        for word in arr:
            if len(set(word)) == len(word):
                filtered.append(word)
        
        def dfs(i, used):
            if i == len(filtered):
                return len(used)
            
            best = dfs(i + 1, used)
            if not (set(filtered[i]) & used):
                best = max(best, dfs(i + 1, used | set(filtered[i]))) # set union
            return best
        
        return dfs(0, set())
```

## 2597. The Number of Beautiful Subsets[[Link](https://leetcode.com/problems/the-number-of-beautiful-subsets/description/)]

```py
"""
Question Understanding
- Input:
    - `num`: positive integer arr
    - `k`: positive integer
- Definition:
    - Beautiful Subsets: within a subset, two integer a and b where abs(a - b) != k
- Output:
    - return the number of non-empty beautiful subsets

Assumptions:
1 <= nums.length <= 10
1 <= nums[i], k <= 1000


General Ideas
- Backtrack every possible subsets with recursive call
- Memorize a visited subset using hahtable
- Problems to solve:
    - What is the decision tree looks like (take first example)
        - branch 1: [2] -> [2, 4], [2]...
        - branch 2: [] -> [4], [] -> ...
    - What is the base case for recursive call
    - Under what condition should call the recursive function
    - What parameter needs, include:
        - final result:
        - parameters passed in recursive funciton

Approach:
- Algo Analysis: Time O(2^n), Space O(n) stack
- Maintain:
    - freq: a hashmap tracking counts of numbers chosen so far
    - idx: current index in nums
    - total: global result counter
- Steps:
    1. Sort nums → Reasoning: ensures consistent order for recursive checks
    2. Define recursive function dfs(i, freq)
       - Base: if i == len(nums), return 1 (represents one valid subset path)
    3. At each index i:
       - Choice 1: skip nums[i]
         - Reasoning: subsets may not include current element
       - Choice 2: include nums[i] if allowed
         - Condition: freq[nums[i] - k] == 0 and freq[nums[i] + k] == 0
         - Reasoning: ensures no forbidden pair forms
         - If allowed, increment freq[nums[i]], recurse, then backtrack
    4. At the end, subtract 1 from final answer
       - Reasoning: dfs counts the empty subset, but we need only non-empty
- This backtracking is efficient due to pruning forbidden inclusions
"""

class Solution:
    def beautifulSubsets(self, nums: List[int], k: int) -> int:
        n = len(nums)
        freq = defaultdict(int)

        def dfs(i):
            if i == n:
                return 1
            
            # skip current element
            total = dfs(i + 1)

            # try to include nums[i] if no conflict
            if not freq[nums[i] - k] and not freq[nums[i] + k]:
                freq[nums[i]] += 1
                total += dfs(i + 1)
                freq[nums[i]] -= 1
            
            return total
        
        return dfs(0) - 1
```

## 241. Different Ways to Add Parentheses[[Link](https://leetcode.com/problems/different-ways-to-add-parentheses/description/)]

```py
"""
Question Understanding:
- Input:
    - `expression`: string of numbers and operators
- Ouput:
    - return all possible results of expression by trying to group numbers and operators

Cases:
- expressions = "", ret:
- expressions = "123", ret: 123
- 

Assumption:
- Input experssion is alwyas valid
- Only operators are '+', '-', '*'
- No division, no parentheses in input
- All results fit in 32-bit signed integer
- The number of distinct results will not exceed 10^4

Approach:
- Algo Analysis: Time ~ O(Catalan(n)) (exponential but manageable for n<=20), Space O(n^2) for memoization
- Clarify variables needed
    - memo: dictionary to store computed results for substrings
    - expression: input string
- Maintain:
    - Recursive function `dfs(expr)` returns all possible results for substring `expr`
    - Base case: if expr contains no operator → return [int(expr)]
- Steps:
    - Iterate through expr:
        - If current char is an operator:
            - Split into left = expr[:i], right = expr[i+1:]
            - Get leftResults = dfs(left)
            - Get rightResults = dfs(right)
            - For each l in leftResults and r in rightResults:
                - If op == '+', append l+r
                - If op == '-', append l-r
                - If op == '*', append l*r
            - Reasoning: This ensures we compute every parenthesization involving this operator
    - If no operator found, return [int(expr)]
    - Memoize results for expr
- This logic follows naturally from the recursive definition of parenthesization.
"""

class Solution:
    def diffWaysToCompute(self, expression: str) -> List[int]:
        memo = {}

        def dfs(exper):
            if exper in memo:
                return memo[exper]
            
            res = []
            for i, ch in enumerate(exper):
                if ch in "+-*":
                    left, right = dfs(exper[:i]), dfs(exper[i + 1:])
                    for l in left:
                        for r in right:
                            if ch == '+':
                                res.append(l + r)
                            if ch == '-':
                                res.append(l - r)
                            if ch == "*":
                                res.append(l * r)
            if not res:
                res = [int(exper)]
            memo[exper] = res
            return res
        return dfs(expression)
```

## 1718. Construct the Lexicographically Largest Valid Sequence[[Link](https://leetcode.com/problems/construct-the-lexicographically-largest-valid-sequence/description/)]

```py
"""
Quesetion Understanding:
- Input:
    - `n`: integer
- Rules:
    - range from [1, n]
    - integer 1 occurs once per sequence
    - for each integer i (2 ≤ i ≤ n), the two occurrences of i must have a distance exactly i (except 1, every other n occurs twice per sequence)
- Output:
    - A sequence (array of integers) with length 2n - 1, with the largest lexicographically order under the rules metnioned above

Case:
- n = 1, ret: 1
- n = 2, ret: [2, 1, 2]
- n = 3, ret: [3, 1, 2, 3, 2]

Assumptions:
- 1 <= n <= 20
- sequnce length == 2 * n - 1
- Input n i a valid integer within constraint

General Idea:
- Check if a number i can be placed at position p
    - if i == 1 -> place once
    - if i > 1 -> check if p + i < len(seq) and both seq[p] and seq[p + i] empty
- Backtracking recursive placement
- Compare lexicograpgical order: try to filling larger number first
- Maintain visited/used array

Approach:
- Algo Analysis: Time O(n^n), Space O(n)
- Maintain:
    - `res`: array of length 2n - 1 initizlied with 0 (empty)
    - `used`: a set for numbers already placed
- Steps:
    - construct a backtracking function dfs(i)
        - start with the larghets number (n)
        - for current number i:
            - if i == 1:
                - place in first avaible non-empty slot in `res`
            - else:
                - iterate position p from 0 to len(res) - i - 1
                - if res[p] == 0 and res[i + 1] == 0, place i at both
        - recurse to the next smaller number
        - if all placed, return true
        - if stuck, fill largest number fisrt, then smaller ones
- Return the result array
"""

class Solution:
    def constructDistancedSequence(self, n: int) -> List[int]:
        size = 2 * n - 1
        res = [0] * size
        used = set()

        def dfs(i):
            if i == size:
                return True

            if res[i] != 0:
                return dfs(i + 1) # skip filled spot

            for num in range(n, 0, - 1):
                if num in used:
                    continue
                if num == 1:
                    res[i] = 1
                    used.add(1)
                    if dfs(i + 1):
                        return True
                    res[i] = 0
                    used.remove(1)
                else:
                    if i + num < size and res[i + num] == 0:
                        res[i] = res[i + num] = num
                        used.add(num)
                        if dfs(i + 1):
                            return True
                        res[i] = res[i + num] = 0
                        used.remove(num)
            return False
        
        dfs(0)
        return res
```

## 2044. Count Number of Maximum Bitwise-OR Subsets[[Link](https://leetcode.com/problems/count-number-of-maximum-bitwise-or-subsets/description/)]

```py
"""
Question Understanding:
- Input:
    - `nums`: int arr
- Rule:
    - get a subsets that has the maximum maximum bitsiwe or
- Ouput:
    - return the count of subsets that achieve that maximum OR.

Cases:
- nums = [1], ret: 1
- nums = [1, 2], ret: 1

Assumption:
1 <= nums.length <= 16
1 <= nums[i] <= 10^5

General Ideas
- Backtrack every possible subset with recursive call
- No need for a hashtable of seen subsets → we don’t care about avoiding duplicates by indices
- Questions to solve:
    - What is the decision tree looks like
        - branch 1: include nums[i]
        - branch 2: not include nums[i]
    - What is the base case for the recursive call
        - i == len(nums), means considered all element,
            - then increment count if current OR equals to max OR
    - Under what condition should call the recursive function
        - At index i
            - Choose to incluide: dfs(i + 1, curr_or | nums[i])
            - Choose to skip: dfs(i + 1, curr_or)
    - What values needed:
        - final result:
            - `max_or`: the target OR
            - `count`: number of subsets that acheive max OR
        - parameters passed in recursive funciton
            - `i`: current OR value so far
            - `curr_or`: current OR values so far
Approach:
- Algo Analysis: Time O(2^n), Spcae O(n)
- Maintain:
    - `max_or`: the target OR
    - `count`: number of subsets that acheive max OR
- Steps:
    - Iterate through nums[i] to get the target `max_or`
    - Construct a recursive function dfs(i, curr_or)
        - If i == len(nums), increment count by 1 by evaluating if curr_or == max_or
        - Call recursive function dfs(i + 1, curr_or), dfs(i + 1, curr_or | nums[i])
    - Call the dfs(0, 0)
    - Return the final result `count`
"""

class Solution:
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        max_or = 0
        for num in nums:
            max_or |= num
        
        self.count = 0

        def dfs(i, curr_or):
            if i == len(nums):
                if curr_or == max_or:
                    self.count += 1
                return 
            
            dfs(i + 1, curr_or)
            dfs(i + 1, curr_or | nums[i])
        
        dfs(0, 0)
        return self.count
```