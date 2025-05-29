# Stack in LC

## 20. Valid Parentheses[[Link](https://leetcode.com/problems/valid-parentheses/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/validate-parentheses)]

```python
# time & space: O(n)
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        close_to_open = {')': '(', ']': '[', '}': '{'}

        for c in s:
            # if the key in close parentheses
            if c in close_to_open:
                # make sure stack is not empty and the top of stack is the equal to the open parentheses
                if stack and stack[-1] == close_to_open[c]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(c)
        # finally if stack is empty means all are matches
        # return true
        # else return false
        return True if not stack else False
```

## 155. Min Stack[[Link](https://leetcode.com/problems/min-stack/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/minimum-stack)]
- hint: two stacks

```python
class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # evaluate the given value and the top of the min stack, and get the smaller one
        val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

## 150. Evaluate Reverse Polish Notation[[Link](https://leetcode.com/problems/evaluate-reverse-polish-notation/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/evaluate-reverse-polish-notation)]

```python
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for t in tokens:
            if t == "+":
                stack.append(stack.pop() + stack.pop())
            elif t == "-":
                a, b = stack.pop(), stack.pop()
                stack.append(b - a) 
            elif t == "*":
                stack.append(stack.pop() * stack.pop())
            elif t == "/":
                a, b = stack.pop(), stack.pop()
                stack.append(int(float(b) / a))
            else:
                stack.append(int(t))
        return stack[0]
```

## 739. Daily Temperatures[[Link](https://leetcode.com/problems/daily-temperatures/description/)]

- video explaination[[Link](https://neetcode.io/problems/daily-temperatures)]

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        res = [0] * len(temperatures)
        stack = [] # pair: [temp, index]

        for i, t in enumerate(temperatures):
            while stack and t > stack[-1][0]:
                stack_t, stack_idx = stack.pop()
                res[stack_idx] = (i - stack_idx)
            stack.append([t, i])
        return res
```

## 853. Car Fleet[[Link](https://leetcode.com/problems/car-fleet/description/)]

- video explainationp[[Link](http://neetcode.io/problems/car-fleet)]

```python
# time: O(n log n); space: O(n)
class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pairs = [(p, s) for p, s in zip(position, speed)]
        pairs.sort(reverse=True) 
        stack = []

        for p, s in pairs:
            stack.append((target - p) / s) # calculate time
            # does it overlap with other one
            if len(stack) >= 2 and stack[-1] <= stack[-2]:
                stack.pop()
        return len(stack)
```

## 71. Simplify Path[[Link](https://leetcode.com/problems/simplify-path/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link](https://neetcode.io/problems/simplify-path)]

```python
# time & space: O(n)
class Solution:
    def simplifyPath(self, path: str) -> str:
        stack = []
        paths = path.split("/")

        for cur in paths:
            if cur == "..":
                if stack:
                    stack.pop()
            elif cur != "" and cur != ".":
                stack.append(cur)
        
        return "/" + "/".join(stack)
        
```