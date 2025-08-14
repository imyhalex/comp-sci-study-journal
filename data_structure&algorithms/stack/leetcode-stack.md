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

## 853. Car Fleet[[Link](https://leetcode.com/problems/car-fleet/description/)]

- video explainationp[[Link](http://neetcode.io/problems/car-fleet)]

```python
# time: O(n log n); space: O(n)
class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pairs = [(p, s) for p, s in zip(position, speed)]
        # We want to simulate cars catching up, and that only makes sense if we process cars from closest to farthest from the target:
        pairs.sort(reverse=True) # This sorts the list of (position, speed) tuples in descending order, by default on the first element of the tuple — which is position.
        stack = []

        for p, s in pairs:
            stack.append((target - p) / s) # calculate time
            # does it overlap with other one
            # If the current car (last one on stack) reaches sooner than the one before it,
            # it gets absorbed into that fleet → pop it (no new fleet formed)
            # len(stack) >= 2 means we only start doing conditon compare when it has >= cars record
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
            elif cur and cur != ".":
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
            start_idx = i # start_idx can be either current index i, or index that is anchored backeward
            while stack and h < stack[-1][1]:
                index, height = stack.pop()
                max_area = max(max_area, height * (i - index)) # i means current index
                start_idx = index # if pop, anchor the start_idx for the current single rectangle to have backward extend potential
            stack.append((start_idx, h)) # push the anchored index and height
        
        # backward extended
        for i, h in stack:
            max_area = max(max_area, h * (len(heights) - i)) # len(height) - i because already reacht he end, backward lookup a the way from the end
        
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

## 901. Online Stock Span[[Link](https://leetcode.com/problems/online-stock-span/description/)]

- video explaination[[Link](https://neetcode.io/problems/online-stock-span?list=neetcode250)]
- monotonic stack

```python
# time & space: O(n)
class StockSpanner:

    def __init__(self):
        self.stack = []

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            _, s = self.stack.pop()
            span += s
        self.stack.append((price, span))
        return self.stack[-1][1]


# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)
```

## 394. Decode String[[Link](https://leetcode.com/problems/decode-string/description/)]

- video explaination[[Link](https://neetcode.io/problems/decode-string?list=neetcode250)]

```python
# time: O(n + N); space: O(n + N)
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []

        for i in range(len(s)):
            if s[i] != "]":
                stack.append(s[i])
            else:
                substr = ""
                while stack and stack[-1] != "[":
                    substr = stack.pop() + substr
                stack.pop() # pop opening bracket

                k = ""
                while stack and stack[-1].isdigit():
                    k = stack.pop() + k
                
                stack.append(int(k) * substr)
        
        return "".join(stack)
```

## 895. Maximum Frequency Stack[[Link](https://leetcode.com/problems/maximum-frequency-stack/description/)]

- video explaination[[Link](https://neetcode.io/problems/maximum-frequency-stack?list=neetcode250)]

```python
# time & space: O(1)
class FreqStack:

    def __init__(self):
        self.count = {} # number -> freq
        self.max_freq = 0
        self.stacks = {} # freq -> stack, freq -> stack

    def push(self, val: int) -> None:
        value_count = 1 + self.count.get(val, 0)
        self.count[val] = value_count
        if value_count > self.max_freq:
            self.max_freq = value_count
            self.stacks[value_count] = []
        self.stacks[value_count].append(val)

    def pop(self) -> int:
        number = self.stacks[self.max_freq].pop()
        self.count[number] -= 1
        if not self.stacks[self.max_freq]: # if the stack in the max frequncy is empty, reduce 1 to get nex stack with smaller frequency
            self.max_freq -= 1
        return number
        

# Your FreqStack object will be instantiated and called as such:
# obj = FreqStack()
# obj.push(val)
# param_2 = obj.pop()
```

## 496. Next Greater Element I[[Link](https://leetcode.com/problems/next-greater-element-i/description/)]

```python
# time: O(n + m); space: O(n)
class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        stack = []
        next_greater_map = {} # number -> its next greater value on the right

        for num in nums2:
            while stack and num > stack[-1]:
                prev = stack.pop()
                next_greater_map[prev] = num
            stack.append(num)
        
        return [next_greater_map.get(n, -1) for n in nums1]
```

## 739. Daily Temperatures[[Link](https://leetcode.com/problems/daily-temperatures/description/)]

- video explaination[[Link](https://neetcode.io/problems/daily-temperatures)]

```python
# time & space: O(n)
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        res = [0] * len(temperatures)
        stack = [] # pair: (temperature, index)

        for i, t in enumerate(temperatures):
            while stack and stack[-1][0] < t:
                _, idx = stack.pop()
                res[idx] = (i - idx)
            stack.append((t, i))
        
        return res

"""
1475. Final Prices With a Special Discount in a Shop (Easy)
496. Next Greater Element I (Easy)
503. Next Greater Element II (Medium)
1019. Next Greater Node In Linked List (Medium)
456. 132 Pattern (Medium)
1504. Count Submatrices With All Ones (Medium)
1673. Find the Most Competitive Subsequence (Medium)
907. Sum of Subarray Minimums (Medium)
1856. Maximum Subarray Min-Product (Medium)
1124. Longest Well-Performing Interval (Medium)
402. Remove K Digits (Medium)
84. Largest Rectangle in Histogram (Hard)
85. Maximal Rectangle (Hard)
"""       
```

## 2390. Removing Stars From a String[[Link](https://leetcode.com/problems/removing-stars-from-a-string/description/)]

```python
# time & space: O(n)
class Solution:
    def removeStars(self, s: str) -> str:
        stack = []

        for ch in s:
            if stack and ch == '*':
                stack.pop()
            if ch != '*':
                stack.append(ch)

        return ''.join(stack)
```