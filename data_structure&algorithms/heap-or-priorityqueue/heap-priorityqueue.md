# Heap Properties[[Link](https://neetcode.io/courses/dsa-for-beginners/23)]

- structure property:
    - A binary heap is a binary tree that is a complete binary tree, 
    - every single level of the tree is filled completely, except possibly the lowest level nodes, which are filled contiguously from left to right.
- order property:
    - The order property for a min-heap is that all of the descendents should be greater than their ancestors.
    - 
```python

# Parent: i

# Left child: 2 * i + 1

# Right child: 2 * i + 2

# Parent of i: (i - 1) // 2
```

# Heap Push/Pop[[Link]()]

```python
class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        self.heap.append(val)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        self._swap(0, len(self.heap) - 1)
        min_val = self.heap.pop()
        self._heapify_down(0)
        return min_val

    def peek(self):
        return self.heap[0] if self.heap else None

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parent]:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        n = len(self.heap)

        if left < n and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < n and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    # or
    # def _swap(self, i, j):
    #     tmp = self.heap[i]
    #     self.heap[i] = self.heap[j]
    #     self.heap[j] = tmp

    def __str__(self):
        return str(self.heap)
```

# Two Heaps[[Link](https://neetcode.io/courses/advanced-algorithms/10)]

- small (max_heap): heap contains smaller values
- large (min_heap): heap contains larger values

```python
import heapq

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