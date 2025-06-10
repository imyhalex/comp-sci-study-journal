# LC in Heap

## 703. Kth Largest Element in a Stream[[Link](https://leetcode.com/problems/kth-largest-element-in-a-stream/description/)]

- video explaination[[Link](https://neetcode.io/problems/kth-largest-integer-in-a-stream?list=blind75)]

```python
# time:O(m * log k); space: O(k)
import heapq
class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.min_heap, self.k = nums, k
        heapify(self.min_heap)
        while len(self.min_heap) > k:
            heappop(self.min_heap)

    def add(self, val: int) -> int:
        heappush(self.min_heap, val)
        if len(self.min_heap) > self.k:
            heappop(self.min_heap)
        return self.min_heap[0]


# Your KthLargest object will be instantiated and called as such:
# obj = KthLargest(k, nums)
# param_1 = obj.add(val)
```

## 1046. Last Stone Weight[[Link](https://leetcode.com/problems/last-stone-weight/description/)]

- video explaination[[Link](https://neetcode.io/problems/last-stone-weight?list=blind75)]

```python
# sorting
# time: O(n^2 log n); space: O(1) or O(n) depending on sorting algo
class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        
        while len(stones) > 1:
            stones.sort()
            curr = stones.pop() - stones.pop()
            if curr:
                stones.append(curr) 
            
        return stones[0] if stones else 0

# heap
# time: O(n log n); space: O(n)
import heapq
class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        stones = [-s for s in stones]
        heapify(stones) 

        while len(stones) > 1:
            first = heappop(stones)
            second = heappop(stones) 
            if second > first:
                heappush(stones, first - second)
        # what is stone is empty? then append zero here to handle it (this can also be handled in return, shown below)
        # if not stones:
        #     stones.append(0)

        return abs(stones[0]) if stones else 0
```