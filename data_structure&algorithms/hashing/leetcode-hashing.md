# Hashing in LC

## 217. Contains Duplicate[[Link](https://leetcode.com/problems/contains-duplicate/)]
- video explaination[[Link](https://neetcode.io/problems/duplicate-integer)]

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        hash_set = set()
        for num in nums:
            if num in hash_set:
                return True
            hash_set.add(num)
        return False
```

## 219. Contains Duplicate II[[Link](https://leetcode.com/problems/contains-duplicate-ii/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/contains-duplicate-ii)]
- hint: this is a fixed size sliding window problem

```python
class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        window = set()
        # two pointers left and right
        l = 0
        for r in range(len(nums)):
            if r - l > k: # lock the size of window
                window.remove(nums[l])
                l += 1
            if nums[r] in window:
                return True
            window.add(nums[r])
        return False
```

## 1. Two Sum[[Link](https://leetcode.com/problems/two-sum/description/?envType=study-plan-v2&envId=top-interview-150)]
- video explaination[[Link](https://neetcode.io/problems/two-integer-sum)]
- important: return indices only if diff offset is in hash_map and the offset is not equal to the current one
```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hash_map = {}

        for i, n in enumerate(nums):
            hash_map[n] = i
        
        for i, n in enumerate(nums):
            diff = target - n
            if diff in hash_map and hash_map[diff] != i:
                return [i, hash_map[diff]]
```

## *146. LRU Cache[[Link](https://leetcode.com/problems/lru-cache/description/?envType=study-plan-v2&envId=top-interview-150)]
- video explaination[[Link](https://neetcode.io/problems/lru-cache)]

```python
class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {} # map the key to node

        # left=LRU, right=most recent
        # for next two steps: dummny nodes for initialization, 
        # and set left and right pointer for anchor points
        self.left, self.right = Node(0, 0), Node(0, 0)
        self.left.next, self.right.prev = self.right, self.left

    # helpers: remove, insert
    def __remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def __insert(self, node): # insert at right
        prev, nxt = self.right.prev, self.right
        prev.next = nxt.prev = node
        node.next, node.prev = nxt, prev

    def get(self, key: int) -> int:
        if key in self.cache:
            # update the node to most recent
            self.__remove(self.cache[key])
            self.__insert(self.cache[key])
            return self.cache[key].val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.__remove(self.cache[key])
        self.cache[key] = Node(key, value)
        self.__insert(self.cache[key])

        if len(self.cache) > self.cap:
            # remove from the linked list  and delete the LRU from hashmap
            lru = self.left.next
            self.__remove(lru)
            del self.cache[lru.key]
        


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
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

## 49. Group Anagrams[[Link](https://leetcode.com/problems/group-anagrams/description/?envType=study-plan-v2&envId=top-interview-150)]

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

## 128. *Longest Consecutive Sequence[[Link](https://leetcode.com/problems/longest-consecutive-sequence/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/longest-consecutive-sequence)]
- hint: check the left neigbor for each num in nums to determine the start, and check num + 1 for right to determine the consecutive numbers

```python
# time & space: O(n)
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        longest = 0

        for num in num_set: # change this from nums to num_set else LC time limit exceed
            # check if its start of a sequence
            if (num - 1) not in num_set: # if no left neigbor, then it is start
                length = 0
                while (num + length) in num_set: # num + length to detect consecutive nums
                    length += 1
                longest = max(longest, length)
        return longest

# Binary Tree Longest Consecutive Sequence
# Medium
# Find Three Consecutive Integers That Sum to a Given Number
# Medium
# Maximum Consecutive Floors Without Special Floors
# Medium
# Length of the Longest Alphabetical Continuous Substring
# Medium
# Find the Maximum Number of Elements in Subset
# Medium
```

## 846. Hand of Straights[[Link](https://leetcode.com/problems/hand-of-straights/description/)]

- video explaination[[Link](https://neetcode.io/problems/hand-of-straights?list=neetcode150)]

```python
# time: O(n log n); space: O(n)
class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        if len(hand) % groupSize:
            return False
        
        count = {}
        for n in hand:
            count[n] = 1 + count.get(n, 0)
        
        min_heap = list(count.keys())
        heapq.heapify(min_heap)
        while min_heap:
            first = min_heap[0]
            for i in range(first, first + groupSize):
                if i not in count:
                    return False
                count[i] -= 1
                if count[i] == 0:
                    if i != min_heap[0]:
                        return False
                    heapq.heappop(min_heap) 
        return True
```

## 1899. Merge Triplets to Form Target Triplet[[Link](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/description/)]

- video explaination[[Link](https://neetcode.io/problems/merge-triplets-to-form-target?list=neetcode150)]

```python
# time: O(n); space: O(1)
class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        good = set()

        for t in triplets:
            if t[0] > target[0] or t[1] > target[1] or t[2] > target[2]:
                continue
            
            for i, v in enumerate(t):
                if v == target[i]:
                    good.add(i)
        return len(good) == 3
```

## 763. Partition Labels[[Link](https://leetcode.com/problems/partition-labels/description/)]

- video explaination[[Link](https://neetcode.io/problems/partition-labels?list=neetcode150)]

```python
# time: O(n); space: O(m)
class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        hash_map = {} # char -> last_index of character

        for i, c in enumerate(s):
            hash_map[c] = i
        
        res = []
        size, end = 0, 0
        for i, c in enumerate(s):
            size += 1
            end = max(end, hash_map[c])
            if i == end:
                res.append(size)
                size = 0
        return res
```

## *678. Valid Parenthesis String[[Link](https://leetcode.com/problems/valid-parenthesis-string/description/)]

- video explaination[[Link](https://neetcode.io/problems/valid-parenthesis-string?list=neetcode150)]

```python
# time: O(n); space: O(1)
class Solution:
    def checkValidString(self, s: str) -> bool:
        left_min, left_max = 0, 0

        for c in s:
            if c == "(":
                left_min, left_max = left_min + 1, left_max + 1
            elif c == ")":
                left_min, left_max = left_min - 1, left_max - 1
            else:
                left_min, left_max = left_min - 1, left_max + 1
            
            if left_max < 0: # ))(( negative left max, return false
                return False
            if left_min < 0: # whenever hit negative, reset it to zero
                left_min = 0 # s = ( * ) (
        
        return left_min == 0
```

## 36. Valid Sudoku[[Link](https://leetcode.com/problems/valid-sudoku/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/valid-sudoku)]

```python
# time & space: O(n ^ 2)
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = defaultdict(set)
        cols = defaultdict(set)
        square = defaultdict(set) # key = (r // 3, c // 3)

        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    continue

                if (board[r][c] in rows[r] or
                    board[r][c] in cols[c] or 
                    board[r][c] in square[(r // 3, c // 3)]):
                    return False

                cols[c].add(board[r][c])
                rows[r].add(board[r][c])
                square[(r // 3, c // 3)].add(board[r][c])

        return True

# the square in sudoku can be represented as sections 0 - 9 by (r //3, c // 3)
"""example
. . . . . . . . .
. 1 . . 2 . . 3 .
. . . . . . . . .
. . . . . . . . .
. 4 . . 5 . . 6 .
. . . . . . . . .
. . . . . . . . .
. 7 . . 8 . . 9 .
. . . . . . . . .

e.g.
1 // 3 = 0 if r, c = 0, 0
every coordinates in first sections fall in square[(1 //3, 1 // 3)]
"""
```

## 2661. First Completely Painted Row or Column[[Link](https://leetcode.com/problems/first-completely-painted-row-or-column/description/)]

<!-- - video explaination[[Link]()] -->

```python
# time: O(m * n + len(arr)); space: O(m * n)
class Solution:
    def firstCompleteIndex(self, arr: List[int], mat: List[List[int]]) -> int:
        m, n = len(mat), len(mat[0])

        # build valid -> (row, col) map
        position = {}
        for r in range(m):
            for c in range(n):
                position[mat[r][c]] = (r, c)
        
        # track how many cells are painted in each row/col
        # row -> total_paint each row
        # col -> total_paint each col
        row_count, col_count = defaultdict(int), defaultdict(int)
        for i, num in enumerate(arr):
            r, c = position[num]
            row_count[r] += 1
            col_count[c] += 1
            if row_count[r] == n or col_count[c] == m:
                return i
        
        return -1
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
                    new_count[n] -= 1
            count = new_count
        
        for n in count.keys():
            if nums.count(n) > len(nums) // 3:
                res.append(n)
        
        return res

```

## 705. Design HashSet[[Link](https://leetcode.com/problems/design-hashset/description/)]

- video explaintation[[Link](https://neetcode.io/problems/design-hashset?list=neetcode250)]

```python
# time & space: O(n)
class MyHashSet:

    def __init__(self):
        self.hash_set = []

    def add(self, key: int) -> None:
        if key not in self.hash_set:
            self.hash_set.append(key)

    def remove(self, key: int) -> None:
        if key in self.hash_set:
            self.hash_set.remove(key)

    def contains(self, key: int) -> bool:
        return key in self.hash_set


# Your MyHashSet object will be instantiated and called as such:
# obj = MyHashSet()
# obj.add(key)
# obj.remove(key)
# param_3 = obj.contains(key)
```


## 706. Design HashMap[[Link](https://leetcode.com/problems/design-hashmap/description/)]
- video explaination[[Link](https://neetcode.io/problems/design-hashmap?list=neetcode250)]

```python
# time: O(1); space: O(1000001)
class MyHashMap:

    def __init__(self):
        self.hash_map = [-1] * 1000001

    def put(self, key: int, value: int) -> None:
        self.hash_map[key] = value

    def get(self, key: int) -> int:
        return self.hash_map[key]

    def remove(self, key: int) -> None:
        self.hash_map[key] = -1


# Your MyHashMap object will be instantiated and called as such:
# obj = MyHashMap()
# obj.put(key,value)
# param_2 = obj.get(key)
# obj.remove(key)
```