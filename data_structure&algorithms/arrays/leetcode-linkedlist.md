# Linkedlist in LC

## 61. Rotate List[[Link](https://leetcode.com/problems/rotate-list/description/?envType=problem-list-v2&envId=two-pointers)]

- video explaination[[Link](https://neetcode.io/solutions/rotate-list)]

```python
# time: O(n); space: O(1)

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head:
            return head
        
        length, tail = 1, head
        while tail.next:
            tail = tail.next
            length += 1
        
        # what if k >= length of linkedlist
        k = k % length
        if k == 0:
            return head
        
        # move to the pivot and move perform swap
        curr = head
        for i in range(length - k - 1):
            curr = curr.next
        
        new_head = curr.next
        curr.next = None
        tail.next = head

        return new_head

# new_head = curr.next
# curr.next = None
# tail.next = head
"""example
1 -> 2 -> 3 -> 4 -> 5   k = 2
new_head
         curr->curr.next
1 -> 2 -> 3 -> 4 -> 5

do new_head = curr.next
            new_head
1 -> 2 -> 3 -> 4 -> 5

do curr.next = None
         curr->curr.next
1 -> 2 -> 3 -> None    4 -> 5

do tail.next = head
tail->head          curr->curr.next  
  4 -> 5 -> 1 -> 2 -> 3 -> None 
"""
```