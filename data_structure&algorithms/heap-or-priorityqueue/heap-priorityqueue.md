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