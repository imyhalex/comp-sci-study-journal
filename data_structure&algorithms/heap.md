# Heap

## Binary Heap

A __Binary Heap__ is a complete binary tree. A binary heap is either in Min Heap or Max Heap.

- A binary heap is typically represented as an array
    - the root element at `arr[0]`
    - `arr[(i - 1) / 2]` returns the parent node
    - `arr[(2 * i) + 1]` returns the left child node
    - `arr[(2 * i) + 2]` returns the right child node

# Operation on Heap (Min Heap):
- `getMin()`: Time Complexity in \(O(1)\). 
- `extractMin()`: Remove the minimum element from Min Heap. Time Complexity is in \(O(log n)\).
- `decreaseKey()`: Decreases the value of the key. The time complexity is in \(O(log n)\). If the decreased key value of a node is greater than the parent of the node, don’t do anything. Otherwise, traverse up to fix the violated heap property.
- `insert()`: Time complexity in \(O(log n)\). We add a new key at the end of the tree. If the new key is greater than its parent, then we don’t need to do anything. Otherwise, we need to traverse up to fix the violated heap property.
- `delete()`: Deleting a key also takes O(log N) time. We replace the key to be deleted with the minimum infinite by calling decreaseKey(). After decreaseKey(), the minus infinite value must reach root, so we call extractMin() to remove the key.

```java
import java.util.*;

class MinHeap {

    int[] heap;

    // max size of the heap;
    int capacity;

    // current number of elements in the heap
    int currentHeapSize;

    MinHeap(int n) { 
        this.capacity = n;
        this.heap = new int[n];
        this.currentHeapSize = 0;
    }

    int partent(int key) {
        return (key - 1) / 2;
    }

    int left(int key) { 
        return key * 2 + 1;
    }

    int right(int key) { 
        return key * 2 + 2;
    }

    private void swap(int[] arr, int a, int b) { 
        int temp = arr[a];
        arr[a] = arr[b];
        arr[b] = temp;
    }

    private void resize() {
        int[] np = new int[capacity * 2];
        for (int i = 0; i < currentHeapSize; i++)
            np[i] = heap[i];
        heap = np;
        capacity *= 2;
    }

    void insert(int key) { 
        if (currentHeapSize == capacity)
            resize();
        
        // first insert the new key at the end
        int i = currentHeapSize;
        heap[i] = key;
        currentHeapSize++;

        // fix the min heap properly if it is violated
        while (i != 0 && heap[parent(i)] > heap[i]) { 
            swap(heap, i, parent(i));
            i = parent(i);
        }
    }

    int getMin() {
        return heap[0];
    }

    private void minHeapify(int key) { 
        int l = left(key);
        int r = right(key);
        int smallest = key;

        if (l < currentHeapSize && heap[l] < heap[smallest])
            smallest = l;
        
        if (r < currentHeapSize && heap[r] < heap[smallest])
            smallest = r;
        
        if (smallest != key) {
            swap(heap, key, smallest);
            minHeapify(smallest);
        } 
    }

    int deleteMin() {
        // if heap is empty, return something or throw an exception
        if (currentHeapSize <= 0)
            return Integer.MAX_VALUE;
        
        // if only one element, just remove it
        if (currentHeapSize == 1) { 
            currentHeapSize--;
            return heap[0];
        }

        // store the minimum value (root), move last element to root and heapify
        int root = heap[0];
        heap[0] = heap[currentHeapSize - 1];
        currentHeapSize--;
        minHeapify(0);
    }
}
```

## Leetcode Questions

### 215. Kth Largest Element in an Array[[Link](https://leetcode.com/problems/kth-largest-element-in-an-array/description/?envType=study-plan-v2&envId=top-interview-150)]

__Algorithm:__
- Initialize a min-heap heap.
- Iterate over the input. For each num:
    - Push num onto the heap.
    - If the size of heap exceeds k, pop from heap.
- Return the top of the heap.

__Answer:__
```java
import java.util.Queue;
import java.util.PriorityQueue;

class Solution {
    public int findKthLargest(int[] nums, int k) {
        Queue<Integer> heap = new PriorityQueue<>();
        for (int num : nums) { 
            heap.add(num);
            if (heap.size() > k)
                heap.remove();
        }

        return heap.peek();
    }
}
```
<br/>

### Find K Paris with Smallest Sums[[link](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/?envType=study-plan-v2&envId=top-interview-150)]

**Approach Explanation (Min-Heap / Priority Queue)**

We want the **k** pairs \((u, v)\) where \(u\) comes from `nums1` and \(v\) comes from `nums2\), such that the sum \(u + v\) is among the smallest possible. Both arrays are sorted in **non-decreasing** order.

A straightforward method is:
1. **Use a min-heap (priority queue)** to always extract the pair with the smallest sum.
2. Each heap entry will store a pair of indices \((i, j)\) representing the pair \((nums1[i], nums2[j])\) along with its sum.

However, we must be careful to avoid inserting all \(n \times m\) possible pairs into the heap at once (which would be too large in many cases). Instead, we use a strategy somewhat like a "multi-way merge":

1. **Initialize** the heap by offering one pair from each "row" or "column" to kickstart the process.  
   - A common pattern is to start **only** with \((i = 0, j = 0)\). We know `nums1[0] + nums2[0]` is the absolute smallest sum.  
   - Insert `(0, 0)` into the min-heap.  

2. **Pop from the heap** (which gives us the current smallest sum) and add that pair to the result.  
   - Let the popped index pair be \((i, j)\).

3. **Then push the next potential candidates**:  
   - If we took \((i, j)\), the "neighbors" in sorted order are \((i + 1, j)\) and \((i, j + 1)\) (because each array is sorted, these indices lead to the next largest sums).  
   - But we must avoid duplicates, so maintain a visited set of index pairs to ensure we don't push the same pair twice.

4. **Repeat** this process until you extract **k** pairs (or you run out of pairs).

__Complexity:__
- If \(k\) is much smaller than \(n \times m\), we avoid generating all pairs at once.  
- Each pop and push from the heap takes \(O(\log(\text{sizeOfHeap}))\). In the worst case, we might push up to \(k\) times, so the time complexity is roughly \(O(k \log k)\) (though in practice, the heap can grow to at most `min(k, n * m)` in size but typically we consider \(k \le n \times m\)).


__Answer:__
```java
import java.util.*;

class Solution {
    public List<List<Integer>> kSmallestPairs(int[] nums1, int[] nums2, int k) {
        List<List<Integer>> result = new ArrayList<>();
        if (nums1 == null || nums2 == null || nums1.length == 0 || nums2.length == 0 || k == 0) {
            return result;
        }
        
        // Min-heap storing (sum, i, j)
        // sum is not strictly necessary because we can compute from i, j, but it helps readability.
        PriorityQueue<int[]> minHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(a[0], b[0])
        );
        
        // We'll store sum, i, j -> but i and j let us retrieve the actual values from nums1, nums2
        // Offer the first pair: (nums1[0] + nums2[0], 0, 0)
        minHeap.offer(new int[]{nums1[0] + nums2[0], 0, 0});

        // Keep track of visited index pairs to avoid re-pushing the same pair
        Set<String> visited = new HashSet<>();
        visited.add("0,0");
        
        while (!minHeap.isEmpty() && result.size() < k) {
            int[] top = minHeap.poll();
            int sum = top[0];
            int i   = top[1];
            int j   = top[2];
            
            // Add the actual pair to result
            result.add(Arrays.asList(nums1[i], nums2[j]));
            
            // Next candidate from the same row: (i, j+1)
            if (j + 1 < nums2.length) {
                String key = i + "," + (j+1);
                if (!visited.contains(key)) {
                    visited.add(key);
                    minHeap.offer(new int[]{nums1[i] + nums2[j+1], i, j+1});
                }
            }
            
            // Next candidate from the same column: (i+1, j)
            if (i + 1 < nums1.length) {
                String key = (i+1) + "," + j;
                if (!visited.contains(key)) {
                    visited.add(key);
                    minHeap.offer(new int[]{nums1[i+1] + nums2[j], i+1, j});
                }
            }
        }
        
        return result;
    }
}
```
<br/>
