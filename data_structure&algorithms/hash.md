## 202. Happy Number[[Link](https://leetcode.com/problems/happy-number/description/?envType=study-plan-v2&envId=top-interview-150)]

- Vide Explaination[[Link](https://www.youtube.com/watch?v=ljz85bxOYJ0)]
```python
class Solution:
    def isHappy(self, n: int) -> bool:
        visited = set()

        while n not in visited:
            visited.add(n)
            n = self.sum_of_square(n)

            if n == 1:
                return True
        
        return False 
        
    def sum_of_square(self, n: int) -> int:
        output = 0

        while n:
            digit = n % 10
            digit = digit ** 2
            output += digit
            n = n // 10
        
        return output
```

- or implemented in linkedlist cycle
```python
# Floyd's Cycle-Finding Algorithm
class Solution:
    def isHappy(self, n: int) -> bool:
        slow = n
        fast = self.get_next(n)
        while slow != fast and fast != 1:
            slow = self.get_next(slow)
            fast = self.get_next(self.get_next(fast))
        return fast == 1
        
    def get_next(self, n: int) -> int:
        output = 0
        while n:
            digit = n % 10
            output += digit ** 2
            n = n // 10 
        return output
```