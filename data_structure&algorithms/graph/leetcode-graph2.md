## 997. Find the Town Judge[[Link](https://leetcode.com/problems/find-the-town-judge/description/)]

- video explaination[[Link](https://neetcode.io/problems/find-the-town-judge?list=neetcode250)]

```python
# time: O(V + E); space: O(V)
class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        incoming = defaultdict(int)
        outgoing = defaultdict(int)

        for src, dst in trust:
            incoming[dst] += 1
            outgoing[src] += 1
        
        for i in range(1, n + 1):
            if incoming[i] == n - 1 and outgoing[i] == 0:
                return i
        
        return -1
```

