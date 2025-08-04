## 133. Clone Graph[[Link](https://leetcode.com/problems/clone-graph/description/?envType=study-plan-v2&envId=top-interview-150)]

__Answer__
- Explaination[[Link](https://neetcode.io/problems/clone-graph)]
- hint: the visited in this question should be a hashmap that map old node to new clone node: old_to_new = 
```python
# DFS
# time: O(V+E); space: O(V)
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""
from typing import Optional
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None
        old_to_new = {}

        def dfs(node):
            if node in old_to_new:
                return old_to_new[node]
            
            # clone -> new node for clone graph
            clone = Node(node.val)
            old_to_new[node] = clone
            # recursively clone the neigbhor
            for neighbor in node.neighbors:
                clone.neighbors.append(dfs(neighbor))
            return clone
        
        return dfs(node)
```

## 138. Copy List with Random Pointer[[Link](https://leetcode.com/problems/copy-list-with-random-pointer/description/)]

- hash useage, two passes
- video explaination[[Link](https://neetcode.io/problems/copy-linked-list-with-random-pointer?list=neetcode250)]

```python
# time & space: O(n)
"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        old_to_copy = {None : None}

        # first pass: construct hashmap, clone linkedlist
        curr = head
        while curr:
            copy = Node(curr.val)
            old_to_copy[curr] = copy
            curr = curr.next
        
        # construct new linkedlist through existing hashmap
        # do ptrs connecting, next and random
        # link the random
        curr = head
        while curr:
            copy = old_to_copy[curr]
            copy.next = old_to_copy[curr.next]
            copy.random = old_to_copy[curr.random]
            curr = curr.next
        
        return old_to_copy[head]
```

## 1485. Clone Binary Tree With Random Pointer[[Link](https://leetcode.com/problems/clone-binary-tree-with-random-pointer/description/)]

```python
# time & space: O(n)
# Definition for Node.
# class Node:
#     def __init__(self, val=0, left=None, right=None, random=None):
#         self.val = val
#         self.left = left
#         self.right = right
#         self.random = random

class Solution:
    def copyRandomBinaryTree(self, root: 'Optional[Node]') -> 'Optional[NodeCopy]':
        old_to_new = {}

        def dfs(node):
            if not node:
                return None
            if node in old_to_new:
                return old_to_new[node]
                
            clone = NodeCopy(node.val)
            old_to_new[node] = clone

            clone.left = dfs(node.left)
            clone.right = dfs(node.right)
            clone.random = dfs(node.random)

            return clone
        
        return dfs(root)
```