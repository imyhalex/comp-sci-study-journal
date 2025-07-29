## 567. Permutation in String[[Link](https://leetcode.com/problems/permutation-in-string/description/)]

- video explaination[[Link](https://neetcode.io/problems/permutation-string)]
```python
# brute-force
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        s1 = sorted(s1)

        for i in range(len(s2)):
            for j in range(i, len(s2)):
                sub_str = s2[i:j + 1]
                sub_str = sorted(sub_str)
                if s1 == sub_str:
                    return True
        return False

# sliding window
# time: O(n); space: O(1)
# 1
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False
        
        s1_count, s2_count = [0] * 26, [0] * 26
        for i in range(len(s1)):
            s1_count[ord(s1[i]) - ord('a')] += 1
            s2_count[ord(s2[i]) - ord('a')] += 1
        
        # at this stage, if two are equal, immediate return
        if s1_count == s2_count:
            return True
        
        for i in range(len(s1), len(s2)):
            # sliding part: add and remove s2
            # add
            s2_count[ord(s2[i]) - ord('a')] += 1
            # remove the leftmost
            s2_count[ord(s2[i - len(s1)]) - ord('a')] -= 1
            if s1_count == s2_count:
                return True
        return False

# 2
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        s1_count, s2_count = [0] * 26, [0] * 26
        for i in range(len(s1)):
            s1_count[ord(s1[i]) - ord('a')] += 1
            s2_count[ord(s2[i]) - ord('a')] += 1
        
        matches = 0
        for i in range(26):
            matches += (1 if s1_count[i] == s2_count[i] else 0)
        
        l = 0
        for r in range(len(s1), len(s2)):
            if matches == 26:
                return True
            
            index = ord(s2[r]) - ord('a')
            s2_count[index] += 1
            if s1_count[index] == s2_count[index]:
                matches += 1
            elif s1_count[index] + 1 == s2_count[index]:
                matches -= 1

            index = ord(s2[l]) - ord('a')
            s2_count[index] -= 1
            if s1_count[index] == s2_count[index]:
                matches += 1
            elif s1_count[index] - 1 == s2_count[index]:
                matches -= 1
            l += 1
        return matches == 26
```

## 76. Minimum Window Substring[[Link](https://leetcode.com/problems/minimum-window-substring/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/minimum-window-with-characters)]

```python
# time & space: O(n)
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if t == "":
            return ""
        
        count_t, window = {}, {} # char -> count
        # we need to use count_t hashmap to compare with s
        for c in t:
            count_t[c] = 1 + count_t.get(c, 0)
        
        have, need = 0, len(count_t)
        res, res_len = [-1, -1], float('inf') # one store the result pointer, one store the
        l = 0
        for r in range(len(s)):
            c = s[r]
            window[c] = 1 + window.get(c, 0)

            if c in count_t and window[c] == count_t[c]:
                have += 1
            
            while have == need:
                # update the result (record l, r pointers), r - l + 1=lenght of current window
                if (r - l + 1) < res_len:
                    res = [l, r]
                    res_len = (r - l + 1)
                # pop from the left of the window
                window[s[l]] -= 1
                if s[l] in count_t and window[s[l]] < count_t[s[l]]:
                    have -= 1
                l += 1

        l, r = res # this is the shortes length pointers
        return s[l: r + 1] if res_len != float('inf') else ""
```