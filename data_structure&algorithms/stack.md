## Leetcode Questions

### 20. Valid Parentheses[[Link](https://leetcode.com/problems/valid-parentheses/?envType=study-plan-v2&envId=top-interview-150)]

__Answer:__
```java
class Solution {
    public boolean isValid(String s) {
        Stack<Character> stack = new Stack<>();

        for (char c : s.toCharArray()) {
            if (c == '(' || c == '[' || c == '{')
                stack.push(c);
            else { 
                if (stack.isEmpty())
                    return false;

                char top = stack.peek();

                boolean case1 = top == '(' && c == ')';
                boolean case2 = top == '[' && c == ']';
                boolean case3 = top == '{' && c == '}';

                if (case1 || case2 || case3)
                    stack.pop();
                else 
                    return false;
            }
        }
        return stack.isEmpty();
    }
}
```