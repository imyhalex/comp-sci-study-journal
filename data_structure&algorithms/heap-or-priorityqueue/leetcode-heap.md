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

## 973. K Closest Points to Origin[[Link](https://leetcode.com/problems/k-closest-points-to-origin/description/)]
- video explaination[[Link](https://neetcode.io/problems/k-closest-points-to-origin?list=blind75)]

```python
# time: O(k log n); space: O(n)
import heapq
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = [(x**2 + y**2, [x, y]) for x , y in points]
        heapify(heap)
        res = []

        while k > 0:
            dist, point = heappop(heap)
            res.append(point)
            k -= 1
        
        return res
```

## 215. Kth Largest Element in an Array[[Link](https://leetcode.com/problems/kth-largest-element-in-an-array/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/kth-largest-element-in-an-array?list=blind75)]

```python
# time: O(n log k); space: O(k)
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        nums = [-n for n in nums]
        heapq.heapify(nums)
        res = 0

        for _ in range(k):
            res = heapq.heappop(nums) 
        
        return -res
```

## 621. Task Scheduler[[Link](https://leetcode.com/problems/task-scheduler/description/)]

- video explaination[[Link](https://neetcode.io/problems/task-scheduling?list=blind75)]

```python
# time: O(n * m); space O(1)
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        count = Counter(tasks)
        max_heap = [-cnt for cnt in count.values()]
        heapq.heapify(max_heap)

        time = 0
        q = deque() # pairs of [-cnt, idle_time]

        while max_heap or q:
            time += 1
            if max_heap:
                cnt = 1 + heapq.heappop(max_heap)
                if cnt:
                    q.append([cnt, time + n])
            
            if q and q[0][1] == time:
                heapq.heappush(max_heap, q.popleft()[0])
        return time
```

## *355. Design Twitter[[Link](https://leetcode.com/problems/design-twitter/description/)]

- video explaination[[Link](https://neetcode.io/problems/design-twitter-feed?list=blind75)]

```python
# time: O(n log n) for getfeed(), rest of them are O(1)
# space:O(N * m + N * M + n)
class Twitter:

    def __init__(self):
        self.count = 0
        self.follow_map = defaultdict(set)
        self.tweet_map = defaultdict(list)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweet_map[userId].append([self.count, tweetId])
        self.count -= 1

    def getNewsFeed(self, userId: int) -> List[int]:
        res = [] # order start from recent
        min_heap = []

        self.follow_map[userId].add(userId)
        for followee_id in self.follow_map[userId]:
            if followee_id in self.tweet_map:
                index = len(self.tweet_map[followee_id]) - 1
                count, tweet_id = self.tweet_map[followee_id][index]
                min_heap.append([count, tweet_id, followee_id, index - 1])

        heapq.heapify(min_heap)
        while min_heap and len(res) < 10:
            count, tweet_id, followee_id, index = heapq.heappop(min_heap)
            res.append(tweet_id)
            
            if index >= 0:
                count, tweet_id = self.tweet_map[followee_id][index]
                heapq.heappush(min_heap, [count, tweet_id, followee_id, index - 1])
        
        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        self.follow_map[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.follow_map[followerId]:
            self.follow_map[followerId].remove(followeeId)

``` 

## 295. Find Median from Data Stream[[Link](https://leetcode.com/problems/find-median-from-data-stream/description/)]

- video explaination[[Link](https://leetcode.com/problems/find-median-from-data-stream/description/)]

```python
class MedianFinder:

    def __init__(self):
        self.small = []  # max heap (invert values to simulate)
        self.large = []  # min heap

    def addNum(self, num: int) -> None:
        # Add to max heap (small) first
        heapq.heappush(self.small, -num)

        # Balance: ensure max(small) ≤ min(large)
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Balance size: max difference is 1
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        elif len(self.large) > len(self.small):
            return self.large[0]
        else:
            return (-self.small[0] + self.large[0]) / 2
```