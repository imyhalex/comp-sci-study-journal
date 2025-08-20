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
# time: O(n); space: O(1)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)

        # phase 1: reach the left ptr
        left_prev, curr = dummy, head
        for _ in range(left - 1):
            left_prev = curr
            curr = curr.next
        
        # phase 2: reverse the portion
        prev = None
        for _ in range(right - left + 1):
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp
        
        # phase 3: repoint the ptrs
        left_prev.next.next = curr # new tail
        left_prev.next = prev # new head
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

## 148. Sort List[[Link](https://leetcode.com/problems/sort-list/description/?envType=problem-list-v2&envId=two-pointers)]

- video explaination[[Link](https://neetcode.io/solutions/sort-list)]

```python
# time: O(n log n); space: O(log n)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        [-1,5,3,4,0]
        # sort linked list using sorting algos
        recursive merge sort
        """
        if not head or not head.next:
            return head

        def get_mid(node):
            slow, fast = node, node.next
            while fast and fast.next:
                slow = slow.next
                fast = fast.next.next
            return slow

        def merge(list1, list2):
            dummy = curr = ListNode()

            while list1 and list2:
                if list1.val < list2.val:
                    curr.next = list1
                    list1 = list1.next
                else:
                    curr.next = list2
                    list2 = list2.next
                curr = curr.next
            
            curr.next = list1 or list2
            return dummy.next

        # split the list into two half
        left = head
        right = get_mid(left)
        tmp = right.next # get the middle fo the LL, which is the end of the first half
        right.next = None
        right = tmp # now the right ptr is truly point to the head of the LL

        left = self.sortList(left)
        right = self.sortList(right)
        return merge(left, right)
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

## 622. Design Circular Queue[[Link](https://leetcode.com/problems/design-circular-queue/description/)]

- video explaination[[Link](https://leetcode.com/problems/design-circular-queue/description/)]

```python
# time: O(n); space: O(1) for each methods
class ListNode:
    def __init__(self, val, next, prev):
        self.val = val
        self.next = next
        self.prev = prev

class MyCircularQueue:

    def __init__(self, k: int):
        self.space = k
        self.left = ListNode(0, None, None)
        self.right = ListNode(0, None, self.left)
        self.left.next = self.right

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        curr = ListNode(value, self.right, self.right.prev)
        self.right.prev.next = curr
        self.right.prev = curr
        self.space -= 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.left.next = self.left.next.next
        self.left.next.prev = self.left
        self.space += 1
        return True

    def Front(self) -> int:
        if self.isEmpty():
            return -1
        return self.left.next.val

    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        return self.right.prev.val

    def isEmpty(self) -> bool:
        return self.left.next == self.right

    def isFull(self) -> bool:
        return self.space == 0
        


# Your MyCircularQueue object will be instantiated and called as such:
# obj = MyCircularQueue(k)
# param_1 = obj.enQueue(value)
# param_2 = obj.deQueue()
# param_3 = obj.Front()
# param_4 = obj.Rear()
# param_5 = obj.isEmpty()
# param_6 = obj.isFull()
```


## *146. LRU Cache[[Link](https://leetcode.com/problems/lru-cache/description/?envType=study-plan-v2&envId=top-interview-150)]
- video explaination[[Link](https://neetcode.io/problems/lru-cache)]

```python
class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {} # map the key to node

        # left=LRU, right=most recent
        # for next two steps: dummny nodes for initialization, 
        # and set left and right pointer for anchor points
        self.left, self.right = Node(0, 0), Node(0, 0)
        self.left.next, self.right.prev = self.right, self.left

    # helpers: remove, insert
    def __remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def __insert(self, node): # insert at right
        prev, nxt = self.right.prev, self.right
        prev.next = nxt.prev = node
        node.next, node.prev = nxt, prev

    def get(self, key: int) -> int:
        if key in self.cache:
            # update the node to most recent
            self.__remove(self.cache[key])
            self.__insert(self.cache[key])
            return self.cache[key].val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.__remove(self.cache[key])
        self.cache[key] = Node(key, value)
        self.__insert(self.cache[key])

        if len(self.cache) > self.cap:
            # remove from the linked list  and delete the LRU from hashmap
            lru = self.left.next
            self.__remove(lru)
            del self.cache[lru.key]
        


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```

## 460. LFU Cache[[Link](https://leetcode.com/problems/lfu-cache/description/)]

- video explaination[[Link](https://neetcode.io/problems/lfu-cache?list=neetcode250)]

```python
# time: O(1); space: O(n)
class Node:
    def __init__(self, val):
        self.val = val
        self.next = self.prev = None

class LinkedList:
    def __init__(self):
        self.left, self.right = Node(0), Node(0)
        self.left.next = self.right
        self.right.prev = self.left
        self.hash_map = {} # value -> Node
    
    def length(self):
        return len(self.hash_map)

    def push_right(self, val):
        node = Node(val)
        self.hash_map[val] = node
        prev, nxt = self.right.prev, self.right
        prev.next = node
        nxt.prev = node
        node.prev, node.next = prev, nxt
    
    def pop(self, val):
        if val in self.hash_map:
            node = self.hash_map[val]
            prev, nxt = node.prev, node.next
            prev.next = nxt
            nxt.prev = prev
            self.hash_map.pop(val)

    def pop_left(self):
        val = self.left.next.val
        self.pop(val)
        return val
    
    def update(self, val):
        self.pop(val)
        self.push_right(val)

class LFUCache:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.lfu_count = 0
        self.val_map = {} # map key - > val
        self.count_map = defaultdict(int)  # Map key -> count
        self.list_map = defaultdict(LinkedList) # Map count of key -> linkedlist

    def counter(self, key):
        cnt = self.count_map[key]
        self.count_map[key] += 1
        self.list_map[cnt].pop(key)
        self.list_map[cnt + 1].push_right(key)
        
        # case when update the lfu_count
        if cnt == self.lfu_count and self.list_map[cnt].length() == 0:
            self.lfu_count += 1
    
    def get(self, key: int) -> int:
        if key not in self.val_map:
            return -1
        self.counter(key)
        return self.val_map[key]

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        
        if key not in self.val_map and len(self.val_map) == self.cap:
            res = self.list_map[self.lfu_count].pop_left()
            self.val_map.pop(res)
            self.count_map.pop(res)
            
        self.val_map[key]= value
        self.counter(key)
        self.lfu_count = min(self.lfu_count, self.count_map[key])


# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```

## 234. Palindrome Linked List[[Link](https://leetcode.com/problems/palindrome-linked-list/description/)]

- video explaination[[Link](https://neetcode.io/problems/palindrome-linked-list?list=allNC)]

```py
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        prev = None
        curr = slow
        while curr:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp
        
        curr = head
        while prev:
            if curr.val != prev.val:
                return False
            curr = curr.next
            prev = prev.next
        return True
```

## 2487. Remove Nodes From Linked List[[Link](https://leetcode.com/problems/remove-nodes-from-linked-list/description/)]

- video explaination[[Link](https://neetcode.io/solutions/remove-nodes-from-linked-list)]

```py
# time: O(n); space: O(1)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        def reverse(head):
            prev, curr = None, head
            while curr:
                tmp = curr.next
                curr.next = prev
                prev = curr
                curr = tmp
            return prev
        
        head = reverse(head)
        curr = head
        curr_max = curr.val

        while curr and curr.next:
            if curr.next.val < curr_max:
                curr.next = curr.next.next
            else:
                curr_max = curr.next.val
                curr = curr.next
        return reverse(head)
```