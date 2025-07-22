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

## 92. Reverse Linked List II[[Link](https://leetcode.com/problems/reverse-linked-list-ii/description/)]

- video explaination[[Link]()]

```python

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


## 287. Find the Duplicate Number[[Link](https://leetcode.com/problems/find-the-duplicate-number/description/)]

- video explaination[[Link](https://neetcode.io/problems/find-duplicate-integer?list=neetcode150)]

```python
# time: O(n); space: O(1)
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow, fast = 0, 0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        
        slow = 0
        while True:
            slow = nums[slow]
            fast = nums[fast]
            if slow == fast:
                break
        
        return slow
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

## 19. Remove Nth Node From End of List[[Link](https://leetcode.com/problems/remove-nth-node-from-end-of-list/description/)]

- video explainationi[[Link](https://neetcode.io/problems/remove-node-from-end-of-linked-list?list=neetcode250)]

```python
# time: O(n); space: O(1)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        left, right = dummy, head

        while n > 0 and right:
            right = right.next
            n -= 1
        
        while right:
            left = left.next
            right = right.next
        
        # delete the node
        left.next = left.next.next
        return dummy.next
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
        curr = head
        while curr:
            copy = old_to_copy[curr]
            copy.next = old_to_copy[curr.next]
            copy.random = old_to_copy[curr.random]
            curr = curr.next
        
        return old_to_copy[head]
```

## *2. Add Two Numbers[[Link](https://leetcode.com/problems/add-two-numbers/description/)]

- video explaination[[Link](https://neetcode.io/problems/add-two-numbers?list=neetcode250)]

```python
# time: O(n + m); space: O(1)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        curr = dummy

        carry = 0
        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0

            # compute the new digit
            val = v1 + v2 + carry

            # tens place
            carry = val // 10
            # extract the carray out
            # ones place
            val = val % 10
            curr.next = ListNode(val)

            # update ptrs
            curr = curr.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
            # 7 + 8 have carry, without adding or carry in while loop, the carry will not be executed
        return dummy.next
```

## 445. Add Two Numbers II[[Link](https://leetcode.com/problems/add-two-numbers-ii/description/)]

```python
# method in reverse
# time & space: O(n + m)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        
        def reverse(head):
            prev, curr = None, head
            while curr:
                tmp = curr.next
                curr.next = prev
                prev = curr
                curr = tmp
            return prev
        
        l1, l2 = reverse(l1), reverse(l2)
        dummy = ListNode()
        curr = dummy
        carry = 0
        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0

            val = v1 + v2 + carry
            carry = val // 10
            val = val % 10
            curr.next = ListNode(val)

            curr = curr.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        
        dummy.next = reverse(dummy.next)
        return dummy.next

# without reverse 
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        s1, s2 = [], []

        while l1:
            s1.append(l1.val)
            l1 = l1.next

        while l2:
            s2.append(l2.val)
            l2 = l2.next

        carry = 0
        head = None

        while s1 or s2 or carry:
            v1 = s1.pop() if s1 else 0
            v2 = s2.pop() if s2 else 0
            total = v1 + v2 + carry
            carry = total // 10
            node = ListNode(total % 10)
            node.next = head
            head = node

        return head
```