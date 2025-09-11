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

## 24. Swap Nodes in Pairs[[Link](https://leetcode.com/problems/swap-nodes-in-pairs/description/)]

```py
"""
Cases:
- LL : 1 -> 3 -> 2 -> 4 -> 5, ret: 3 -> 1 -> 4 -> 5 -> 2
    - 1, 2; 3, 4; 5 three pairs
    - 3 -> 1 -> 4 -> 2 -> 5
    - 3 -> 1 -> 4 -> 5 -> 2

Approach:
- Clarify variables needed:
    - `dummy`: a dummy node before head (helps manage head swaps easily)
    - `prev`: pointer to track node before the current pair
    - `first`, `second`: the two nodes to be swapped
- Maintain:
    - dummy.next → head
    - prev → dummy
- Steps:
    - While both `first` and `second` exist:
        - Set `first = prev.next`, `second = prev.next.next`
        - Update `prev.next = second`
          - Reasoning: connect previous node to the new front of the pair
        - Update `first.next = second.next`
          - Reasoning: link first node to the node after the pair
        - Update `second.next = first`
          - Reasoning: link second node back to first, completing the swap
        - Move `prev = first`
          - Reasoning: move prev forward to prepare for next pair
    - Return dummy.next
- This logic comes directly from the problem’s requirement: we must swap only pointers, not values, so dummy node + pointer juggling ensures correctness.
"""


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy 

        while prev.next and prev.next.next:
            first = prev.next
            second = prev.next.next

            prev.next = second
            first.next = second.next
            second.next = first

            prev = first

        return dummy.next        
```

## 1721. Swapping Nodes in a Linked List[[Link](https://leetcode.com/problems/swapping-nodes-in-a-linked-list/description/)]

```py
"""
Question Understanding
- Input:
    - `head` of the Linked List
    - `k`: int (1-index position)
- Output:
    - Return the head of the linked list after swapping the values of the k-th node from the start and from the end
- Constraint:
    - Must swap node *values* (not pointers) in this problem (different from “Swap Nodes in Pairs”)
    - Valid k (1 ≤ k ≤ length of list)

Clarification:
- Can the `k` == length of the LL?
- What if k == 1?
- Are all node values uniques?
- Will k always within the valid range?

Edge Cases:
- List of length 1, k = 1 → no swap needed
- k = 1 → swap head and tail values
- k = n → same as k = 1
- Even length list, swapping middle two nodes when k = n/2
- Odd length list, k pointing to exact middle → swapping with itself, no effect

Underlying Simple Operations:
- Traversing the linked list (increment pointer)
- Counting total length
- Indexing to positions (k-1 and n-k)
- Swapping two values

Brute Force Approach:
- Traverse the linked list and store all nodes in an array
- Swap array[k-1].val and array[n-k].val
- Return head
- Time: O(n), Space: O(n)

My Approach & Design:
Approach:
- Algo Analysis: Time O(n), Space O(1)
- Variables:
    - n: total length of list
    - left, right: references to k-th from start and k-th from end nodes
    - curr: traversal pointer
- Maintain:
    - First pass: find length n
    - Second pass: iterate again and pick nodes for indices (k-1) and (n-k)
- Steps:
    - Traverse list once to compute n
        - Reasoning: needed to identify k-th from end
    - Traverse list again:
        - If index == k-1, mark left
        - If index == n-k, mark right
        - Reasoning: correct nodes to swap
    - Swap values of left and right
        - Reasoning: problem explicitly allows swapping values
    - Return head
- Logic derived directly from requirement: swap k-th from start and k-th from end, values only.
"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def swapNodes(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        curr = head
        n = 0
        while curr:
            curr = curr.next
            n += 1
        
        curr = head
        left, right = None, None
        for i in range(n):
            if i == (k - 1):
                left = curr
            if i == (n - k):
                right = curr
            curr = curr.next
        
        left.val, right.val = right.val, left.val
        return head
```