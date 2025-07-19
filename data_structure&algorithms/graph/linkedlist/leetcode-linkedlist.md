# LinkedList in LC

## 206. Reverse Linked List[[Link](https://leetcode.com/problems/reverse-linked-list/description/)]

- video explaination[[Link](https://neetcode.io/problems/reverse-a-linked-list?list=neetcode250)]

```python
# time: O(n); space: o(1)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev, curr = None, head

        while curr:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp
        
        return prev
```

## 21. Merge Two Sorted Lists[[Link](https://leetcode.com/problems/merge-two-sorted-lists/description/)]

- video explaination[[Link](https://leetcode.com/problems/merge-two-sorted-lists/description/)]

```python
# time: o(n + m); space: O(1)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = node = ListNode()

        # think list1, list2, node as i, j, k in merge sort
        while list1 and list2:
            if list1.val < list2.val:
                node.next = list1
                list1 = list1.next
            else:
                node.next = list2
                list2 = list2.next
            node = node.next
        
        node.next = list1 or list2

        return dummy.next

```