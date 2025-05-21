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
            if r - l > k:
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
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)
        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord('a')] += 1
            res[tuple(count)].append(s) # conver to tuple because list is mutable so cannot be the key
        return list(res.values())
```