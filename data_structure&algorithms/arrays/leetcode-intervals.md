## 57. Insert Interval[[Link](https://leetcode.com/problems/insert-interval/description/)]

- video explaination[[Link](https://neetcode.io/problems/insert-new-interval?list=neetcode250)]

```python
# time: O(n); space: O(1) extra space, O(n) space for output list 
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # Step 1: Binary search to find correct insertion point for newInterval
        target = newInterval[0]
        l, r = 0, len(intervals) - 1

        while l <= r:
            m = l + (r - l) // 2
            if intervals[m][0] < target:
                l = m + 1
            else:
                r = m - 1

        # Insert newInterval at the correct position to keep intervals sorted
        intervals.insert(l, newInterval)

        # Step 2: Merge overlapping intervals
        res = []
        for interval in intervals:
            # If res is empty or no overlap with the last interval in res
            if not res or res[-1][1] < interval[0]:
                res.append(interval)
            else:
                # Overlap detected; merge current interval with last one in res
                res[-1][1] = max(res[-1][1], interval[1])
        
        return res
```

## 56. Merge Intervals[[Link](https://leetcode.com/problems/merge-intervals/description/)]

- video explaination[[Link](https://neetcode.io/problems/merge-intervals?list=neetcode250)]

```python
# time: O(n log n)
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x : x[0])
        res = []

        for interval in intervals:
            if not res or res[-1][1] < interval[0]:
                res.append(interval)
            else:
                res[-1][1] = max(res[-1][1], interval[1])
        
        return res
```

## 435. Non-overlapping Intervals[[Link](https://leetcode.com/problems/non-overlapping-intervals/description/)]

- video explaination[[Link](https://neetcode.io/problems/non-overlapping-intervals?list=neetcode250)]

```python
# time: o(n log n); space: O(1) or O(n) depending on the sorting algorithm
class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x : x[0])

        res = 0
        prev_end = intervals[0][1]
        for start, end in intervals[1:]:
            if start >= prev_end: # case do not remove
                prev_end = end
            else: # case to remove
                res += 1 
                prev_end = min(prev_end, end)
        
        return res
```
Great question! Let's walk through the example **step by step** and clarify the part you're confused about.

---

### 🔢 Input:

```python
intervals = [[1,3], [2,4], [3,5]]
```

After sorting (which is already in order), we run:

```python
res = 0
prev_end = intervals[0][1]  # prev_end = 3
```

Now loop through:

```python
for start, end in intervals[1:]:
```

So we loop over:

1. `(start=2, end=4)`
2. `(start=3, end=5)`

---

### 🧭 First Iteration:

**Current interval**: `[2,4]`
**prev\_end**: `3`

Check:

```python
if start >= prev_end:  # 2 >= 3 → False
```

→ Overlap detected → increment `res`:

```python
res += 1  # res = 1
prev_end = min(4, 3) = 3  # we keep the one ending earlier
```

---

### 🧭 Second Iteration:

**Current interval**: `[3,5]`
**prev\_end**: `3`

Check:

```python
if start >= prev_end:  # 3 >= 3 → True
```

✅ No overlap → we keep `[3,5]`
Update:

```python
prev_end = 5
```

---

### ✅ Final Result:

```python
res = 1
```

You had to **remove 1 interval** — either `[1,3]` or `[2,4]` — to make the rest non-overlapping.

---

### 🔁 Summary of Loop:

So to clarify:

* **The loop runs twice**: once for `[2,4]` and once for `[3,5]`.
* `res` is incremented **only once**, when overlap is detected.
* `prev_end` is updated **each time**, either by keeping the earlier-ending interval (if overlap), or simply moving forward (if no overlap).


## 252. Meeting Rooms[[Link](https://leetcode.com/problems/meeting-rooms/description/)]

- video explaination[[Link](https://neetcode.io/problems/meeting-schedule?list=neetcode250)]

```python
# time: O(n log n); 
class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        if not intervals:
            return True

        intervals.sort()
        prev_end = intervals[0][1]

        for start, end in intervals[1:]:
            if start < prev_end:
                return False
            prev_end = end
        return True
```

## 253. Meeting Rooms II[[Link](https://leetcode.com/problems/meeting-rooms-ii/description/)]

- video explaination[[Link](https://neetcode.io/problems/meeting-schedule-ii?list=neetcode250)]

```python
# time: O(n log n); space: O(n)
class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        intervals.sort()
        
        # min-heap of end times
        min_heap = []
        heapq.heappush(min_heap, intervals[0][1])
        
        # for each meeting, reuse room if possible
        for start, end in intervals[1:]:
            # if the room that frees up the earliest is free before this starts
            if min_heap[0] <= start:
                heapq.heappop(min_heap)
            # allocate a room (new or just-freed)
            heapq.heappush(min_heap, end)
        # #rooms = #simultaneous end-times we're tracking
        return len(min_heap)
```