## 347. Top K Frequent Elements[[Link](https://leetcode.com/problems/top-k-frequent-elements/description/)]
- video explaination[[Link](https://neetcode.io/problems/top-k-elements-in-list)]
- concepts: hash table, bucket sort
- hint: a hashmap to record the num: freqnecy pair

```python
# time & space: O(n)
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = {}
        freq = [[] for _ in range(len(nums) + 1)]

        # feed in the count hashmap and take record for its freqency
        # for each num, check if it is in hashmap, then 1 + num or 0 
        for num in nums:
            count[num] = 1 + count.get(num, 0)

        # bucket sort part
        # take out each num, frequency (or num, cnt) pair from the hashmap
        for num, cnt in count.items():
            freq[cnt].append(num)

        res = []
        for i in range(len(freq) - 1, 0, -1):
            for num in freq[i]:
                res.append(num)
                if len(res) == k:
                    return res
        return None
```

## 451. Sort Characters By Frequency[[Link](https://leetcode.com/problems/sort-characters-by-frequency/)]

- video explaination[[Link](https://neetcode.io/solutions/sort-characters-by-frequency)]

```python
# time & space: O(n)
class Solution:
    def frequencySort(self, s: str) -> str:
        count = Counter(s) # char -> freq
        freq = [[] for _ in range(len(s) + 1)]

        for char, cnt in count.items():
            freq[cnt].append(char)
        
        res = ""
        for i in range(len(freq) - 1, 0, -1):
            for char in freq[i]:
                res += char * i
        return res
```

## *659. Split Array into Consecutive Subsequences[[Link](https://leetcode.com/problems/split-array-into-consecutive-subsequences/description/)]

- not a bukect sort problem, but similar pattern
- video explaination[[Link]]

```python
# time: O(n log n); space: O(n)
class Solution:
    def isPossible(self, nums: List[int]) -> bool:
        ends = defaultdict(list) # ends[num] -> min_heap of lengths of subsequences ending at num
        
        for num in nums:
            if ends[num - 1]:
                # Extend the shortest subsequence ending at num - 1
                min_len = heapq.heappop(ends[num - 1])
                heapq.heappush(ends[num], min_len + 1)
            else:
                # Start a new subsequence of length 1
                heapq.heappush(ends[num], 1)
        
        # At the end, all subsequences must have length >= 3
        for min_heap in ends.values():
            if min_heap and min_heap[0] < 3:
                return False
        return True
```
