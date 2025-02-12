# Algo Comparison

- __What is In-Place Algorithm?__[[Link](https://www.geeksforgeeks.org/in-place-algorithm/)]
- __Stable and Unstable Algorithms__[[Link](https://www.geeksforgeeks.org/stable-and-unstable-sorting-algorithms/)]

<br/>

```text
Q: Can we make any sorting algorithm stable? 

Any given sorting algorithm which is not stable can be modified to be stable. There can be algorithm-specific 
ways to make it stable, but in general, any comparison-based sorting algorithm which is not stable by nature 
can be modified to be stable by changing the key comparison operation so that the comparison of two keys 
considers position as a factor for objects with equal keys.
```

## Selection Sort
* In place
* __Time Complexity:__ n^2
* __Not Stable__
* Sorted + unsorted sections
  * Find min right of the wall and swap with first left of the wall
  * [Details](https://www.geeksforgeeks.org/selection-sort-algorithm-2/) Analysis
    * One pro to mention: Requires less number of swaps (or memory writes) compared to many other standard algorithms. Only [[cycle sort](https://www.geeksforgeeks.org/selection-sort-algorithm-2/)] beats it in terms of memory writes. Therefore it can be simple algorithm choice when memory writes are costly.
* [Visualization](https://visualgo.net/en/sorting)

### Pseudocode
```text
function selectionSort(arr):
    n = arr.length
    for i from 0 to n-2(n-1)
    do:
        minIndex = i
        for j from i+1 to n-1(n) 
        do:
            if A[j] < A[minIndex]
            then
                minIndex = j
            end if
        end for

        if minIndex != i
        then
            swap A[i] and A[minIndex]
        end if
    end for
end
```

### Code Implementation
```java
class SelectionSort {

    SelectionSort() {}

    private void swap(int[] arr, int l, int r) {
        int temp = arr[l];
        arr[l] = arr[r];
        arr[r] = temp;
    }

    void selectionSort(int[] arr) { 
        int n = arr.length;

        for (int i = 0; i < n - 1; i++) {
            int minIndex = i;

            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIndex])
                    minIndex = j;
            }

            if (minIndex != i) {
                swap(arr, i, minIndex);
            }
        }
    }
}
```

## Bubble Sort
* In place
* __Time Complexity:__ n^2
* Stable
* Sorted + unsorted sections
    * [[Complexity Analysis of Bubble Sort](https://www.geeksforgeeks.org/time-and-space-complexity-analysis-of-bubble-sort/)]
    * Find min right of the wall and remember it in temp
    * Move items from left of the wall to min to the right
    * Plop the temp left of the wall
* [Details](https://www.geeksforgeeks.org/bubble-sort-algorithm/)

### Pseudocode 
```text
function bubbleSort(arr):
    do

        swapped = false

        for i = 1 to indexOfLastUnsortedElement-1
        do:

            if leftElement > rightElement
            then:
                swap(leftElement, rightElement)
                swapped = true; ++swapCounter
            end if
        end for

    while swapped
end
```

### Code Implementation
```java
class BubbleSort { 

    BubbleSort() {}

    private void swap(int[] arr, int l, int r) { 
        int temp = arr[l];
        arr[l] = arr[r];
        arr[r] = temp;
    }

    void bubbleSort(int[] arr) { 
        int n = arr.length - 1;
        do { 
            boolean swapped = false;

            for (int i = 1; i < n - 1; i++) {
                if (arr[i] > arr[i + 1]) {
                    swap(arr, i, i + 1);
                    swapped = true;
                }
            }
        } while (swapped);
    }
}
```

## Insertion Sort
* In place
* n^2
* __Stable__
* Bad when in reverse order, good when almost sorted
* More efficient then selection sort
* Similar to playing cards
* Move the wall, and find the right place to put the first element left of the wall
  * Does not use min, just first element left of the wall, find its home rigt of wall
* [Details](https://www.geeksforgeeks.org/insertion-sort-algorithm/)
* [Visualization](https://visualgo.net/en/sorting)

### Pseudocode
```text
function insertionSort(arr):
    n = length(arr)

    for i from 1 to n-1(n)
    do
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[i] > key
        do:
            arr[j + 1] = arr[j]
            j = j - 1
        end while

        arr[j + 1] = key
    end for
end

"""
mark first element as sorted

for each unsorted element X

  'extract' the element X

  for j = lastSortedIndex down to 0

    if current element j > X

      move sorted element to the right by 1

    break loop and insert X here
"""
```

### Code Implementation
```java
class InsertionSort { 

    InsertionSort() {}

    void insertionSort(int[] arr) { 
        int n = arr.length;

        for (int i = 1; i < n; i++) {
            int key = arr[i];

            int j = i - 1;
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j]
                j -= 1;
            }
            arr[j + 1] = key;
        }
    }
}
```

## Quick Sort
* In place
    * do not occuy extra memory(copy of result to arrays)
* n^2 - worst case
    * Avearge Case `n log n`
    * Quicksort is generally very fast in practice due to good caching behavior and low overhead, and many implementations use strategies (like picking a random pivot or “median-of-three”) to avoid consistently hitting the worst-case scenario
    * Quicksort uses cache-friendly sequential memory access, and with reasonably good pivot selection strategy, we rarely hit the worst case O(n^2)
* Want to use tail recursion
* __Not stable__
* Humpty dumpty on the wall, oh how **quickly** they will fall
* Keep splitting the array similar to merge sort, BUT
  * You pivot is the last element in the array, and you want to put elements smaller to right
  * Elements bigger to left
  * and place the pivot element on the wall.
  * Then recurse down the two sections to its left and right doing the same thing
* [Details](https://www.geeksforgeeks.org/quick-sort-algorithm/)
* [Pivot Selection Explaination](https://www.youtube.com/watch?v=VNrF8ugTUkI)
* [Visualization](https://visualgo.net/en/sorting)

### Pseudocode
```text
"""
for each (unsorted) partition

set first element as pivot

  storeIndex = pivotIndex+1

  for i = pivotIndex+1 to rightmostIndex

    if ((a[i] < a[pivot]) or (equal but 50% lucky))

      swap(i, storeIndex); ++storeIndex

  swap(pivot, storeIndex-1)
"""

function partition(arr, low, high):
    pivot = arr[high]

    i = low - 1
    for j from low to high - 1
    do:
        if arr[j] < pivot
        then
            i = i + 1
            swap(arr[i], arr[j])
        end if
    end for

    swap(arr[i + 1], arr[high])
    
    return i + 1
end

function quicksort(arr, low, high):
    if low < high
    then
        pivotIndex = partition(arr, low, high)

        quicksort(arr, low, high - 1)
        quicksort(arr, pivotIndex + 1, high)
    end if
end
```

### Code Implementation
```java
class QuickSort { 

    QuickSort() {}

    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    private int partition(int[] arr, int low, int high) {
        // choose a pivot
        int pivot = arr[high];

        // index of smaller element and indicates the right position of pivot found so far
        int i = low - 1;
        for (int j = low; j < high; j++) { 
            if (arr[j] < pivot) { 
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, high);
        return i + 1; // return new pivot position
    }

    void quickSort(int[] arr, int low, int high) { 
        if (low < high) {
            int pi = partition(arr, low, high);

            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    public static void main(String[] args) {
        int[] arr = {10, 7, 8, 9, 1, 5};
        QuickSort qs = new QuickSort();
        int n = arr.length;
      
        quickSort(arr, 0, n - 1);   
        
        for (int val : arr) {
            System.out.print(val + " ");  
        }
    }
}
```

## Merge Sort
* O(n) spae (not in place)
* nlogn runtime
* stable
* split array until u get to a single element based off a midpoint
  * We do not care about the pivot element or comparison here, just split, which gets logn
  * Once all are single element, merge them back up two at a time (O(n) space)
* [Visualization](https://visualgo.net/en/sorting)

## Heap Sort
* __Time Compexity:__ n log n
* in-place algorithm
* not stable
* Rearrange array elements so that they form a Max Heap(continuously).
* Repeat the following steps until the heap contains only one element:
    * Swap the root element of the heap (which is the largest element in current heap) with the last element of the heap.
    * Remove the last element of the heap (which is now in the correct position). We mainly reduce heap size and do not remove element from the actual array.
    * Heapify the remaining elements of the heap.
* [Details](https://www.geeksforgeeks.org/heap-sort/?ref=outind#detailed-working-of-heap-sort)
* [Video Explaination](https://www.youtube.com/watch?v=2DmK_H7IdTo)

### Pseudocode
```text
n -> heap size

function heapify(arr, i, n):
    largest = i

    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]
    then
        largest = left
    end if

    if right < n and arr[right] > arr[largest]
    then
        largest = right
    end if

    if largest != i
    then
        swap(arr[i], arr[largest])
        heapify(arr, largest, n)
    end if
end

function buildMaxHeap(arr, n):
    for i from floor(n/2) - 1 down to 0
    do:
        heapify(arr, i, n)
    end for
end

function heapSort(arr):
    n = length(arr)

    buildMaxHeap(arr, n)

    for i from n-1 down to 1
    do:
        swap(arr[0], arr[i])
        heapify(arr, 0, i)
    end for
end
```

### Code Implementation

```java
class HeapSort { 

    HeapSort() {}

    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    private void heapify(int[] arr, int i, int n) { 
        int largest = i;

        int l = 2 * i + 1;
        int r = 2 * i + 2;

        if (l < n && arr[l] > arr[largeset])
            largest = l;
        
        if (r < n && arr[r] > arr[largest])
            largest = r;

        if (largest != i) { 
            swap(arr, i, largest);
            heapify(arr, largest, n);
        }
    }

    private void builMaxHeap(int[] arr, n) { 
        for (int i = n / 2 - 1; i >= 0; i--)
            heapify(arr, i, n);
    }

    void heapSort(int[] arr) { 
        int n = arr.length;

        buildMaxHeap(arr, n);

        for (int i = n - 1; i > 0; i--) {
            swap(arr, 0, i);
            heapify(arr, 0, i);
        }
    }
}
```