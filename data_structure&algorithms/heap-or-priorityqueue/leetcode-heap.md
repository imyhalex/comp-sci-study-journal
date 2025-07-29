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

## 480. Sliding Window Median[[Link](https://leetcode.com/problems/sliding-window-median/description/)]

- video explaination[[Link](https://neetcode.io/solutions/sliding-window-median)]

```python

```

## 502. IPO[[Link](https://leetcode.com/problems/ipo/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/ipo?list=neetcode150)]

```python
# time: O(n loh n); space: O(n)
class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        max_profit = [] # only project we can afford
        min_capital = [(c, p) for c, p in zip(capital, profits)]
        heapq.heapify(min_capital)

        for _ in range(k):
            while min_capital and min_capital[0][0] <= w:
                c, p = heapq.heappop(min_capital)
                heapq.heappush(max_profit, -p)
            
            if not max_profit:
                break
            w += -heapq.heappop(max_profit)
        return w
```

## 1834. Single-Threaded CPU[[Link](https://leetcode.com/problems/single-threaded-cpu/description/)]

- video explaination[[Link](https://neetcode.io/problems/single-threaded-cpu?list=neetcode250)]

```python
# time: O(n log n); space: O(n)
class Solution:
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        for i, t in enumerate(tasks):
            t.append(i)
        tasks.sort(key=lambda t : t[0])

        res, min_heap = [], []
        i, time = 0, tasks[0][0]

        while min_heap or i < len(tasks):
            # add tasks to queue
            while i < len(tasks) and time >= tasks[i][0]:
                heapq.heappush(min_heap, [tasks[i][1], tasks[i][2]])
                i += 1
            
            if not min_heap:
                time = tasks[i][0]
            else:
                process_time, index = heapq.heappop(min_heap)
                time += process_time
                res.append(index)
        
        return res
```

## 767. Reorganize String[[Link](https://leetcode.com/problems/reorganize-string/description/)]

- video explaination[[Link](https://neetcode.io/problems/reorganize-string?list=neetcode250)]

```python
# time: O(n); space: O(1) or O(n)
class Solution:
    def reorganizeString(self, s: str) -> str:
        count = Counter(s) # hash_map, count each char
        max_heap = [[-cnt, char] for char, cnt in count.items()]
        heapq.heapify(max_heap) # O(n)

        prev = None
        res = ""
        while max_heap or prev:
            # a -> 2, b -> 0: means max_heap is empty and the prev it not empty
            if not max_heap and prev:
                return ""

            # most frequent char except prev
            cnt, char = heapq.heappop(max_heap)
            res += char
            cnt += 1

            # if prev is not null, push back to heap and set prev as null for next iteration
            if prev:
                heapq.heappush(max_heap, prev)
                prev = None

            # for the pair just popped
            if cnt != 0:
                prev = [cnt, char]
        
        return res
```

## 1405. Longest Happy String[[Link](https://leetcode.com/problems/longest-happy-string/description/)]

- video explaination[[Link](https://neetcode.io/problems/longest-happy-string?list=neetcode250)]

```python
# time: O(n); space: O(1) or O(n)
class Solution:
    def longestDiverseString(self, a: int, b: int, c: int) -> str:
        max_heap = []
        for cnt, char in [(-a, 'a'), (-b, 'b'), (-c, 'c')]:
            if cnt != 0:
                heapq.heappush(max_heap, (cnt, char))
        
        res = ""
        while max_heap:
            cnt, char = heapq.heappop(max_heap)
            # when cannot add the most common charater
            if len(res) > 1 and res[-1] == res[-2] == char:
                if not max_heap:
                    break

                cnt2, char2 = heapq.heappop(max_heap)
                res += char2
                cnt2 += 1

                if cnt2 != 0:
                    heapq.heappush(max_heap, (cnt2, char2))
            else:
                res += char
                cnt += 1
                
            if cnt != 0:
                heapq.heappush(max_heap, (cnt, char))

        return res
```

## 1094. Car Pooling[[Link](https://leetcode.com/problems/car-pooling/description/)]

- video explaination[[Link](https://neetcode.io/problems/car-pooling?list=neetcode250)]

```python
# time: O(n log n); space: (n)
class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        trips.sort(key=lambda t : t[1])
        min_heap = [] # pair of [end, num_passengers]

        curr_passengers = 0
        for t in trips:
            num_passengers, start, end = t # at this time, this value has not pushed into heap yet
            while min_heap and min_heap[0][0] <= start:
                curr_passengers -= min_heap[0][1]
                heapq.heappop(min_heap)

            curr_passengers += num_passengers

            if curr_passengers > capacity:
                return False
            
            heapq.heappush(min_heap, [end, num_passengers])
        
        return True
```