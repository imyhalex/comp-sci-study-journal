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
        return len(stack) == 0
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
# time & space: O(n)
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
        pairs.sort(reverse=True) # This sorts the list of (position, speed) tuples in descending order, by default on the first element of the tuple — which is position.
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

## 84. Largest Rectangle in Histogram[[Link](https://leetcode.com/problems/largest-rectangle-in-histogram/description/)]

- video explaination[[Link](https://neetcode.io/problems/largest-rectangle-in-histogram)]

```python
# time: O(n); Space:O(n)
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        max_area = 0
        stack = [] # pair: (index, height)

        for i, h in enumerate(heights):
            start_idx = i
            while stack and stack [-1][1] > h:
                index, height = stack.pop()
                max_area = max(max_area, height * (i - index))
                start_idx = index
            stack.append((start_idx, h))
        
        # backward extended
        for i, h in stack:
            max_area = max(max_area, h * (len(heights) - i))
        
        return max_area
```

## 224. Basic Calculator[[Link](https://leetcode.com/problems/basic-calculator/description/?envType=study-plan-v2&envId=top-interview-150)]

- video explaination[[Link]()]

```python
# time & space: O(n)
class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        operand, res = 0, 0
        sign = 1 # 1 means positive, -1 means negative

        for c in s:
            if c.isdigit():
                # forming operand, since it could be more than one digit
                operand = (operand * 10) + int(c)
            elif c == "+":
                # evaluate the expression to the left
                # with result, sign, operand
                res += sign * operand
                # save the recently encontered "+" sign 
                sign = 1
                # reset the operand
                operand = 0
            elif c == "-":
                res += sign * operand
                sign = -1
                operand = 0
            elif c == "(":
                # push the result and sign to the stack, for later
                # push the result first, then sign 
                stack.append(res) 
                stack.append(sign) 
                # reset the operand and result, as if new evaluation begins
                # for the new sub-expression
                sign = 1
                res = 0
            elif c == ")":
                # eval the express to the left
                # with result, sign, and operand
                res += sign * operand
                # ")" marks end of the expression within a set of parentheses
                # its result is multiplied with sign on top of stack 
                # as stack.pop() is the sign before parenthese
                res *= stack.pop() # pop 1, sign
                # then add to the next operand on the top
                # as stack.pop() is the result cacluated before this parenthesis
                res += stack.pop() # pop 2, operand
                operand = 0
        
        return res + sign * operand # this is to add the last element that can't handled by conditions above
```

## 682. Baseball Game[[Link](https://leetcode.com/problems/baseball-game/)]
- video explaination[[Link](https://neetcode.io/problems/baseball-game?list=neetcode250)]

```python
# time & space: O(n)
class Solution:
    def calPoints(self, operations: List[str]) -> int:
        stack = []
        for op in operations:
            if op == "C":
                stack.pop()
            elif op == "D":
                stack.append(stack[-1] * 2)
            elif op == "+":
                stack.append(stack[-1] + stack[-2])
            else:
                stack.append(int(op))
        
        return sum(stack)
```

## 225. Implement Stack using Queues[[Link](https://leetcode.com/problems/implement-stack-using-queues/description/)]

- video explaination[[Link](https://neetcode.io/problems/implement-stack-using-queues?list=neetcode250)]

```python
class MyStack:

    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)

    def pop(self) -> int:
        for _ in range(len(self.q) - 1):
            self.push(self.q.popleft())
        return self.q.popleft()

    def top(self) -> int:
        return self.q[-1]

    def empty(self) -> bool:
        return len(self.q) == 0


# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()
```

## 232. Implement Queue using Stacks[[Link](https://leetcode.com/problems/implement-queue-using-stacks/description/)]

- video explaination[[Link](https://leetcode.com/problems/implement-queue-using-stacks/description/)]

```python
# O(1) time for initialization.
# O(1) time for each push() and empty() function calls.
# O(1) amortized time for each pop() and peek() function calls.
class MyQueue:

    def __init__(self):
        self.s1 = []
        self.s2 = []

    def push(self, x: int) -> None:
        self.s1.append(x)

    def pop(self) -> int:
        if not self.s2:
            while self.s1:
                self.s2.append(self.s1.pop())
        return self.s2.pop()

    def peek(self) -> int:
        if not self.s2:
            while self.s1:
                self.s2.append(self.s1.pop())
        return self.s2[-1]

    def empty(self) -> bool:
        return max(len(self.s1), len(self.s2)) == 0


# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()
```

## 735. Asteroid Collision[[Link](https://leetcode.com/problems/asteroid-collision/description/)]

- video explaination[[Link](https://neetcode.io/problems/asteroid-collision?list=neetcode250)]

```python
# time & space: O(n)
class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack = []
        for a in asteroids:
            while stack and a < 0 and stack[-1] > 0:
                diff = a + stack[-1]
                if diff < 0:
                    stack.pop()
                elif diff > 0:
                    a = 0
                else:
                    stack.pop()
                    a = 0
            if a:
                stack.append(a)
        return stack
```