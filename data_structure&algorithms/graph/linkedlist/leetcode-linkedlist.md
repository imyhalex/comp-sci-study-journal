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

## 876. Middle of the Linked List[[Link](https://leetcode.com/problems/middle-of-the-linked-list/description/)]

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow
```

## 141. Linked List Cycle[[Link](https://leetcode.com/problems/linked-list-cycle/description/)]

- video explaination[[Link](https://neetcode.io/problems/linked-list-cycle-detection?list=neetcode250)]

```python
# time: O(n); space: O(1)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow, fast = head, head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        
        return False

# or hashset: O(n) space
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        visited = set()
        curr = head
        while curr:
            if curr in visited:
                return curr
            visited.add(curr)
            curr = curr.next
        return None
```

## 142. Linked List Cycle II[[Link](https://leetcode.com/problems/linked-list-cycle-ii/description/)]

- algo explain[[Link](https://neetcode.io/courses/advanced-algorithms/5)]

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        visited = set()
        curr = head
        while curr:
            if curr in visited:
                return curr
            visited.add(curr)
            curr = curr.next
        return None

# or space O(1)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head

        # phase 1: detect the cycle
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        
        # check if there is no cycle
        # did we reach the end of the list
        if not fast or not fast.next:
            return None
        
        # phase 2: find the entry node of the cycle
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next

        return slow # or fast; both are cycle start 
``` 

## 143. Reorder List[[Link](https://leetcode.com/problems/reorder-list/description/)]

- video explaination[[Link](https://neetcode.io/problems/reorder-linked-list?list=neetcode250)]

- algo explain[[Link](https://neetcode.io/courses/advanced-algorithms/5)]

```python
# time: O(n); space: O(1)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # slow ptr should belongs to first partition of the arr
        second = slow.next # start of second half of the list
        slow.next = None # set the first half end
        prev = None
        # reversing second portion of the list
        while second:
            tmp = second.next
            second.next = prev
            prev = second
            second = tmp
        
        # merge two halfs
        # beginning of the second arr, is prev ptr
        # first arr is origin head
        first, second = head, prev
        while second: # because we know the second half is shorter than first half
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first = tmp1
            second = tmp2
        
```

## 2130. Maximum Twin Sum of a Linked List[[Link](https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/description/)]

- video explaination[[Link](https://neetcode.io/solutions/maximum-twin-sum-of-a-linked-list)]

```python
# time: O(n); space: O(1)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def pairSum(self, head: Optional[ListNode]) -> int:
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        prev, second = None, slow.next
        slow.next = None
        while second:
            tmp = second.next
            second.next = prev
            prev = second
            second = tmp
        
        first, second = head, prev
        res = 0
        while second:
            res = max(res, first.val + second.val)
            first = first.next
            second = second.next
        
        return res
```