## 6. Zigzag Conversion[[Link](https://leetcode.com/problems/zigzag-conversion/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/zigzag-conversion?list=allNC)]

```python
# time & space: O(n)
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1:
            return s
        
        res = ""
        for r in range(numRows):
            increment = 2 * (numRows - 1)
            for i in range(r, len(s), increment):
                res += s[i]
                if (r > 0 and r < numRows - 1 and i + increment - 2 * r < len(s)):
                    res += s[i + increment - 2 * r]
        
        return res
```

## 408. Valid Word Abbreviation[[Link](https://leetcode.com/problems/valid-word-abbreviation/description/)]

- video explaination[[Link](https://neetcode.io/problems/valid-word-abbreviation?list=allNC)]

```python
# time: O(n + m); space: O(1)
class Solution:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        i, j = 0, 0
        n, m = len(word), len(abbr)

        while i < n and j < m:
            if word[i] == abbr[j]:
                i, j = i + 1, j + 1
            elif abbr[j].isalpha() or abbr[j] == '0':
                return False
            else:
                sub_len = 0
                while j < m and abbr[j].isdigit():
                    sub_len = sub_len * 10 + int(abbr[j])
                    j += 1
                i += sub_len
        
        return i == n and j == m
```

## 3110. Score of a String[[Link](https://leetcode.com/problems/score-of-a-string/description/)]

```python
class Solution:
    def scoreOfString(self, s: str) -> int:
        """
        build hash table char -> ord(char)
        iterate through the hash table and compute the abs values
        """
        table = {i: ord(c) for i, c in enumerate(s)}

        res = 0
        prev = None
        for v in table.values():
            if prev:
                res += abs(v - prev)
            prev = v
        
        return res
```

## 1299. Replace Elements with Greatest Element on Right Side[[Link](https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/description/)]

```python
class Solution:
    def replaceElements(self, arr: List[int]) -> List[int]:
        n = len(arr)
        res = [0] * n
        right_max = -1

        for i in range(n - 1, -1, -1):
            res[i] = right_max
            right_max = max(right_max, arr[i])
        return res
```