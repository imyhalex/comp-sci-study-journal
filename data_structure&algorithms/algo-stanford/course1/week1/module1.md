# Merge Sort: Motivation and Example

__What is Merge Sort[[Link](https://www.geeksforgeeks.org/merge-sort/?ref=outind)]__

__Merge Sort Visualization[[Link](https://visualgo.net/en/sorting)]__

# Pseudocode for Merge

1. Divide:  Divide the list or array recursively into two halves until it can no more be divided. 
2. Conquer:  Each subarray is sorted individually using the merge sort algorithm. 
3. Merge:  The sorted subarrays are merged back together in sorted order. The process continues until all elements from both subarrays have been merged. 

```text
C = output[length = n]
A = first sorted array [n/2]
B = second sorted array[n/2]

i = 1
j = 1

for k = 1 to n
    if A(i) < B(i)
        C(k) = A(i)
        i++
    else [B(j) < A(i)]
        C(k) = B(j)
        j++
end
```

```text
function MERGE-SORT(A, low, high)
    if low < high then:
        mid = floor((low + high) / 2)
        MERGE-SORT(A, low, mid)       // Recursively sort the left half
        MERGE-SORT(A, mid + 1, high)    // Recursively sort the right half
        MERGE(A, low, mid, high)        // Merge the two sorted halves

function MERGE(A, low, mid, high)
    n1 = mid - low + 1
    n2 = high - mid
    // Create temporary arrays L[1..n1] and R[1..n2]
    L = new array of length n1
    R = new array of length n2

    // Copy data to temporary arrays
    for i = 1 to n1 do:
        L[i] = A[low + i - 1]
    for j = 1 to n2 do:
        R[j] = A[mid + j]

    // Merge the temporary arrays back into A[low..high]
    i = 1          // Initial index of first subarray
    j = 1          // Initial index of second subarray
    k = low      // Initial index of merged subarray

    while i ≤ n1 and j ≤ n2 do:
        if L[i] ≤ R[j] then:
            A[k] = L[i]
            i = i + 1
        else:
            A[k] = R[j]
            j = j + 1
        k = k + 1

    // Copy any remaining elements of L, if there are any
    while i ≤ n1 do:
        A[k] = L[i]
        i = i + 1
        k = k + 1

    // Copy any remaining elements of R, if there are any
    while j ≤ n2 do:
        A[k] = R[j]
        j = j + 1
        k = k + 1
```

## Merge Sort Running Time

__2 operations:__
```text
i = 1
j = 1
```

__4n operations:__
```text
for k = 1 to n
    if A(i) < B(i)
        C(k) = A(i)
        i++
    else [B(j) < A(i)]
        C(k) = B(j)
        j++
end
```

__Running time:__
```text
running time of merge on array of n numbers is <= 4n + 2 -> <= 6n

claim: merge sort requires <= 6nlog_2 n + 6n
```

\[
T(n) \le 6n \log_2 n + 6n.
\]

A key fact given is that the merge operation on an array of \( n \) numbers takes at most \( 4n + 2 \) steps, which we can further upper-bound by \( 6n \) steps for simplicity.

Below are two common ways to prove the bound: using a **recursion tree (binary tree)** and an **induction proof**.

---

Merge sort works by:
1. Dividing the array into two halves.
2. Recursively sorting each half.
3. Merging the two sorted halves.

If we let \( T(n) \) be the running time on an array of size \( n \), then:
- The two recursive calls contribute \( 2T\left(\frac{n}{2}\right) \).
- The merging step takes at most \( 6n \) steps.

Thus, the recurrence is

\[
T(n) \le 2T\left(\frac{n}{2}\right) + 6n, \quad \text{for } n > 1,
\]

with a base case \( T(1) \le 6 \) (since sorting a single element is a constant-time operation).

Imagine a binary tree where:
- **Root (Level 0):** The problem of size \( n \) with cost \( 6n \).
- **Level 1:** Two subproblems of size \( \frac{n}{2} \) each, each costing \( 6\left(\frac{n}{2}\right) \). Total cost at this level:
  
  \[
  2 \times 6\left(\frac{n}{2}\right) = 6n.
  \]

- **Level 2:** Four subproblems of size \( \frac{n}{4} \) each, each costing \( 6\left(\frac{n}{4}\right) \). Total cost:
  
  \[
  4 \times 6\left(\frac{n}{4}\right) = 6n.
  \]

- **General Level \( i \):** There are \( 2^i \) nodes, each handling a subproblem of size \( \frac{n}{2^i} \) with cost

  \[
  6\left(\frac{n}{2^i}\right).
  \]

  So the total cost at level \( i \) is

  \[
  2^i \times 6\left(\frac{n}{2^i}\right) = 6n.
  \]

The recursion stops when the subproblem size becomes 1. That is, when

\[
\frac{n}{2^i} = 1 \quad \Longrightarrow \quad 2^i = n \quad \Longrightarrow \quad i = \log_2 n.
\]

Thus, there are \(\log_2 n\) levels (not counting the leaves, which are constant time).

- The cost at each of the \(\log_2 n\) levels is \(6n\).
- The total cost from all levels is

  \[
  6n \cdot \log_2 n.
  \]

- In addition, there is the cost at the leaves (base cases). There are \( n \) leaves (each of constant cost, say at most 6), so the total cost at the base level is at most \( 6n \).

Thus, the overall cost is

\[
T(n) \le 6n \log_2 n + 6n.
\]

---

We can also prove the claim by induction.

For \( n = 1 \), we have

\[
T(1) \le 6.
\]

Since \(\log_2 1 = 0\), the bound becomes

\[
6 \cdot 1 \cdot \log_2 1 + 6 \cdot 1 = 0 + 6 = 6,
\]

which holds.


Assume that for all sizes smaller than \( n \) (and assuming \( n \) is a power of 2 for simplicity), the hypothesis holds:

\[
T\left(\frac{n}{2}\right) \le 6\left(\frac{n}{2}\right) \log_2\left(\frac{n}{2}\right) + 6\left(\frac{n}{2}\right).
\]

Now, for an array of size \( n \):

\[
\begin{aligned}
T(n) &\le 2T\left(\frac{n}{2}\right) + 6n \\
     &\le 2\left[6\left(\frac{n}{2}\right) \log_2\left(\frac{n}{2}\right) + 6\left(\frac{n}{2}\right)\right] + 6n \\
     &= 6n \log_2\left(\frac{n}{2}\right) + 6n + 6n \\
     &= 6n \left(\log_2 n - 1\right) + 12n \quad \text{(since } \log_2\frac{n}{2} = \log_2 n - 1\text{)} \\
     &= 6n \log_2 n - 6n + 12n \\
     &= 6n \log_2 n + 6n.
\end{aligned}
\]

Thus, the inductive step is complete.

---

Both the recursion tree analysis and the inductive proof show that merge sort runs in time

\[
T(n) \le 6n \log_2 n + 6n.
\]

This completes the proof of the claimed runtime for merge sort using a binary tree (recursion tree) argument.
```text
Time Complexity:
    Best Case: O(n log n), When the array is already sorted or nearly sorted.
    Average Case: O(n log n), When the array is randomly ordered.
    Worst Case: O(n log n), When the array is sorted in reverse order.
Auxiliary Space: O(n), Additional space is required for the temporary array used during merging.
```

## Implementation of MergeSort in java
```java
class MergeSort {
    private void merge(int[] arr, int l, int m, int r) {
        // size of two subarrays to be merged
        // l, m, r are length
        int n1 = m - l + 1;
        int n2 = r - m;

        int[] L = new int[n1];
        int[] R = new int[n2];

        for (int i = 0; i < n1; i++)
            L[i] = arr[l + i];
        for (int j = 0; j < n2; j++)
            R[i] = arr[m + j + 1];

        // merge temp arrays
        // initial indices for first and second subarrays
        int i = 0, j = 0;
        int k = l;

        while (i < n1 && j < n2) {
            if (L[i] < R[j]) { 
                arr[k] = L[i];
                i++;
            }
            else { 
                arr[k] = R[j];
                j++;
            }
            k++;
        }

        while (i < n1)
            arr[k++] = L[i++];

        while (i < n2)
            arr[k++] = R[j++];
    }

    public void sort(int[] arr, int l, int r) {
        if (l < r) { 
            int m = l + (r - l) / 2;

            sort(arr, l, m);

            sort(arr, m + 1, r);

            merge(arr, l, m , r);
        }
    }

    // A utility function to print array of size n
    static void printArray(int arr[])
    {
        int n = arr.length;
        for (int i = 0; i < n; ++i)
            System.out.print(arr[i] + " ");
        System.out.println();
    }

    // Driver code
    public static void main(String args[])
    {
        int arr[] = { 12, 11, 13, 5, 6, 7 };

        System.out.println("Given array is");
        printArray(arr);

        sort(arr, 0, arr.length - 1);

        System.out.println("\nSorted array is");
        printArray(arr);
    }
}
```