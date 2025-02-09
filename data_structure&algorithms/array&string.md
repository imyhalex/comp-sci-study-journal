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

### 134. Gas Station[[Link](https://leetcode.com/problems/gas-station/description/?envType=study-plan-v2&envId=top-interview-150)]

#### Key Observations

1. **If the total amount of gas is less than the total cost, it is impossible to complete the circuit.** Formally, if 
   \[
   \sum_{i=0}^{n-1} gas[i] < \sum_{i=0}^{n-1} cost[i],
   \]
   then the answer must be `-1`.

2. **Uniqueness**: If it is possible to make the full circuit, exactly one valid starting index exists.

3. **Greedy Observation**: Suppose you start at station 0, and you run out of gas at station \(k\). This means the total amount of gas from stations `0` through `k` was not enough to get you from station \(k\) to station \(k+1\). In that situation, starting anywhere between `0` and `k` also cannot succeed (because you would have run out of gas even earlier). Therefore, the next possible starting point must be \(k+1\).

4. **One-Pass Solution**: We can track our net gas in a single forward pass:
   - A variable `currentTank` to check if our tank goes negative at any point.
   - A variable `start` that records the current candidate starting station.
   - A variable `totalTank` to check if overall we have enough gas to complete the circuit.

---

#### Step-by-Step Solution Outline

1. **Initialize**:
   - `start = 0`: We'll begin by assuming station 0 is the starting candidate.
   - `currentTank = 0`: Tracks your current gas tank when starting from `start`.
   - `totalTank = 0`: Tracks the net surplus or deficit over the entire route.

2. **Iterate over each station `i`**:
   - Compute the difference `diff = gas[i] - cost[i]`.  
   - Update `totalTank += diff` (the global net).
   - Update `currentTank += diff` (the local net starting from the current candidate).
   - **If at any point `currentTank` becomes negative**:
     - It means you cannot reach station `i+1` from the current `start`.  
     - Therefore, set `start = i + 1`.  
     - Reset `currentTank = 0` because you are starting fresh from the new station.

3. **Check feasibility**:
   - After the loop finishes, if `totalTank >= 0`, then `start` is the valid answer.
   - Otherwise, return `-1`.

---

#### Time Complexity
- The key insight is that you only do **one pass** over the arrays (O(n) time).  
- You do not restart the journey from different stations repeatedly; you keep track of one potential start.  

#### Space Complexity
- O(1) extra space.

```java
class Solution {
    public int canCompleteCircuit(int[] gas, int[] cost) {
        int n = gas.length;

        int totalTank = 0;
        int currentTank = 0;
        int start = 0;

        for (int i = 0; i < n; i++) { 
            int diff = gas[i] - cost[i];
            totalTank += diff;
            currentTank += diff;

            if (currentTank < 0) {
                start = i + 1;
                currentTank = 0;
            }
        }
        return (totalTank >= 0) ? start : -1;
    }
}
```
<br/>

### 135. Candy[[Link](https://leetcode.com/problems/candy/description/?envType=study-plan-v2&envId=top-interview-150)]
```text
There are n children standing in a line. Each child is assigned a rating value given in the integer array ratings.

You are giving candies to these children subjected to the following requirements:

Each child must have at least one candy.
Children with a higher rating get more candies than their neighbors.
Return the minimum number of candies you need to have to distribute the candies to the children.

 

Example 1:

Input: ratings = [1,0,2]
Output: 5
Explanation: You can allocate to the first, second and third child with 2, 1, 2 candies respectively.
Example 2:

Input: ratings = [1,2,2]
Output: 4
Explanation: You can allocate to the first, second and third child with 1, 2, 1 candies respectively.
The third child gets 1 candy because it satisfies the above two conditions.

Note: the concept of neighbor does not care about the order, whenever the rating greater than the child next to him/she, that child should get one increment
```
__Answer:__
```java
class Solution {
    public int candy(int[] ratings) {
        int n = ratings.length;

        int[] candies = new int[n];
        Arrays.fill(candies, 1);
        for (int i = 1; i < n; i++) {
            if (ratings[i] > ratings[i - 1])
                candies[i] = candies[i - 1] + 1; 
        }

        int sum = candies[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            if (ratings[i] > ratings[i + 1])
                candies[i] = Math.max(candies[i], candies[i + 1] + 1);
            sum += candies[i];
        }
        return sum;
    }
}
```
<br/>

### *42. Trapping Rain Water[[Link](https://leetcode.com/problems/trapping-rain-water/description/?envType=study-plan-v2&envId=top-interview-150)]

__Answer:__
```java
class Solution {
    public int trap(int[] height) {
        
    }
}
```
<br/>

### 13. Roman to Integer[[Link](https://leetcode.com/problems/roman-to-integer/description/?envType=study-plan-v2&envId=top-interview-150)]

__Answer__
```java
class Solution {
    static Map<Character, Integer> values = new HashMap<>();

    static {
        values.put('M', 1000);
        values.put('D', 500);
        values.put('C', 100);
        values.put('L', 50);
        values.put('X', 10);
        values.put('V', 5);
        values.put('I', 1);
    }

    public int romanToInt(String s) {
        int res = 0;
        int preVal =0;

        for (int i = s.length() - 1; i >= 0; i--) {
            int currentVal = values.get(s.charAt(i));

            if (currentVal < preVal)
                res -= currentVal;
            else 
                res += currentVal;
            
            preVal = currentVal;
        }

        return res;
    }
}
```