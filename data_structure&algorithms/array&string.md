## Leetcode Questions


### 88. Merge Sorted Array[[Link](https://leetcode.com/problems/merge-sorted-array/description/?envType=study-plan-v2&envId=top-interview-150)]

__Video Explaination[[Link](https://www.youtube.com/watch?v=TTWKBqG-6IU)]__

__Answer:__
```java
class Solution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        int i = m - 1;          // Pointer for nums1 (initially at end of actual elements)
        int j = n - 1;          // Pointer for nums2 (initially at end)
        int k = m + n - 1;      // Pointer for the merged array position

        // Compare elements from the end and put the larger one in nums1[k]
        while(i >= 0 && j >= 0) { 
            if (nums1[i] > nums2[j]) { 
                nums1[k] = nums1[i];
                i--;
            }
            else { 
                nums1[k] = nums2[j];
                j--;
            }
            k--;
        }

        // if there are still element left in nums2, copy them
        while (j >= 0) { 
            nums1[k] = nums2[j];
            j--;
            k--;
        }
    }
}
```
<br/>

### 27. Remove Element[[Link](https://leetcode.com/problems/remove-element/description/?envType=study-plan-v2&envId=top-interview-150)]

__Answer:__
```java
class Solution {
    public int removeElement(int[] nums, int val) {
        int len = 0;
        for (int j = 0; j < nums.length; j++) { 
            if (nums[j] != val) {
                nums[len] = nums[j];
                len++;
            }
        }
        return len;
    }
}
```
<br/>

### 26. Remove Duplicates from Sorted Array[[Link](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)]

__Answer:__
```java
class Solution {
    public int removeDuplicates(int[] nums) {
        int countUnique = 1;
        for (int i = 1; i < nums.length; i++) { 
            int prev = nums[i - 1];
            int curr = nums[i];
            if (prev != curr) { 
                nums[countUnique] = nums[i];
                countUnique++;
            }
        }
        return countUnique;
    }
}
```
<br/>

### 80. Remove Duplicates from Sorted Array II[[Link](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/?envType=study-plan-v2&envId=top-interview-150)]

__Answer:__
```java
class Solution {
    public int removeDuplicates(int[] nums) {
        if (nums.length == 0)
            return 0;

        int i = 1;
        int count = 1;
        for (int j = 1; j < nums.length; j++) { 
            int prev = nums[j - 1];
            int curr = nums[j];
            if (prev == curr)
                count++;
            else 
                count = 1;
            
            if (count <= 2)
                nums[i++] = nums[j];
        }
        return i;
    }
}
```
<br/>

### 189. Rotate Array[[Link](https://leetcode.com/problems/rotate-array/description/?envType=study-plan-v2&envId=top-interview-150)]

__Answer 1:__
```java
class Solution {
    public void rotate(int[] nums, int k) {
        int n = nums.length;
        k = k % n;

        int[] temp = new int[n];
        for (int i = 0; i < n; i++)
            temp[(i + k) % n] = nums[i];

        // copy temp back into nums
        for (int i = 0; i < n; i++) 
            nums[i] = temp[i];
    }
}
```
<br/>

__Answer 2: Three reverse method:__

- Idea:
    - Normalize \(k\) by taking `k = k % nums.length`
        - Rotating by `k` steps or by `k % nums.length` steps is the same if `k ≥ array length`.
    - Reverse the entire array.
    - Reverse the first `k` elements.
    - Reverse the remaining `n−k` elements

```text
# original:
[1, 2, 3, 4, 5, 6, 7], with k = 3

# reverse entire array
[7, 6, 5, 4, 3, 2, 1]

# reverse k = 3 elements
Reverse [7, 6, 5] → [5, 6, 7]
→ [5, 6, 7, 4, 3, 2, 1]

# reverse last n - k = 4 elements
Reverse [4, 3, 2, 1] → [1, 2, 3, 4]
→ [5, 6, 7, 1, 2, 3, 4]
```

```java
class Solution {
    private void reverse(int[] nums, int left, int right) { 
        while (left < right) { 
            int temp = nums[left];
            nums[left] = nums[right];
            nums[right] = temp;
            left++;
            right--;
        }
    }

    public void rotate(int[] nums, int k) {
        int n = nums.length;
        k = k % n;

        // reverse entire array
        reverse(nums, 0, n - 1);
        // reverse first k element
        reverse(nums, 0, k - 1);
        // reverse remaining n - k elements
        reverse(nums, k, n - 1);
    }
}
```
<br/>

### 122. Best Time to Buy and Sell Stock II[[Link](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/description/?envType=study-plan-v2&envId=top-interview-150)]

__Answer:__
- Hint: Using Peak-Vally Effect
    - Total Profit = SUM(height of peak - height of valley)
```java
class Solution {
    public int maxProfit(int[] prices) {
        int valley = prices[0];
        int peak = prices[0];
        int maxProfit = 0;

        int i = 0;
        while (i < prices.length - 1) {
            while (i < prices.length - 1 && prices[i] >= prices[i + 1])
                i++;
            valley = prices[i];
            while (i < prices.length - 1 && prices[i] <= prices[i + 1])
                i++;
            peak = prices[i];
            maxProfit += peak - valley;
        }
        return maxProfit;
    }
}
```
<br/>

### 274. H-Index[[Link](https://leetcode.com/problems/h-index/description/?envType=study-plan-v2&envId=top-interview-150)]

__Answer:__
```java
class Solution {
    public int hIndex(int[] citations) {
        Arrays.sort(citations);
        int i = 0;
        while (i < citations.length && citations[citations.length - 1 - i] > i)
            i++;
        return i;
    }
}
```

### 380. Insert Delete GetRandom O(1)[[Link](https://leetcode.com/problems/insert-delete-getrandom-o1/description/?envType=study-plan-v2&envId=top-interview-150)]

__Walk-Through[[link](https://leetcode.com/problems/insert-delete-getrandom-o1/editorial/?envType=study-plan-v2&envId=top-interview-150)]__
- The combination of insert, remove method between hashmap/set and arraylist for O(1) time complexity
- For remove(), it will take liner time, to gain O(1) time complexity:
    - Swap the element to delete to the last one
    - pop the last element out


__Answer:__
```java
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;

class RandomizedSet {

    HashMap<Integer, Integer> map;
    List<Integer> list;
    Random rand = new Random();

    public RandomizedSet() {
        map = new HashMap<>();
        list = new ArrayList<>();
    }
    
    public boolean insert(int val) {
        if (map.containsKey(val))
            return false;
        
        map.put(val, list.size());
        list.add(list.size(), val);
        return true;
    }
    
    public boolean remove(int val) {
        if (!map.containsKey(val))
            return false;
        
        int lst = list.get(list.size() - 1);
        int idx = list.indexOf(val);
        list.set(list.size() - 1, val);
        list.set(idx, lst);
        map.put(lst, idx);

        list.remove(list.size() - 1);
        map.remove(val);
        return true;
    }
    
    public int getRandom() {
        return list.get(rand.nextInt(list.size()));
    }
}
```

### 238. Product of Array Except Self[[Link](https://leetcode.com/problems/product-of-array-except-self/description/?envType=study-plan-v2&envId=top-interview-150)]

__Answer:__
```java
// [4,5,1,8,2] L and R arrays would finally be:
// L: [1, 4, 20, 20, 160]
// R: [80, 16, 16, 2, 1]

class Solution {
    public int[] productExceptSelf(int[] nums) {
        if (nums == null)
            return new int[];

        int n = nums.length;
        int[] L = new int[n];
        int[] R = new int[n];
        int[] res = new int[n];

        L[0] = 1;
        for (int i = 1; i < n; i++) {
            // L[i - 1] already contains the product of elements to the left of 'i - 1'
            // Simply multiplying it with nums[i - 1] would give the product of all
            L[i] = nums[i - 1] * L[i - 1];
        }

        R[n - 1] = 1;
        for (int i = n - 2; i >= 0; i--) { 
            R[i] = nums[i + 1] * R[i + 1];
        }

        for (int i = 0; i < n; i++) { 
            res[i] = L[i] * R[i];
        }
        return res;
    }
}
```