# Trees in LC

## 700. Search in a Binary Search Tree[[Link](https://leetcode.com/problems/search-in-a-binary-search-tree/description/)]
- vide explaination[[Link](https://neetcode.io/solutions/search-in-a-binary-search-tree)]

```python
# time & space: O(H), Where H is the height of the given tree.
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root or root.val == val:
            return root
        
        return self.searchBST(root.left, val) if val < root.val else self.searchBST(root.right, val)
```

## 701. Insert into a Binary Search Tree[[Link](https://leetcode.com/problems/insert-into-a-binary-search-tree/description/)]
- vide explaination[[Link](https://neetcode.io/problems/insert-into-a-binary-search-tree?list=blind75)]

```python
# time & space: O(h)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return TreeNode(val)

        if val > root.val:
            root.right = self.insertIntoBST(root.right, val)
        elif val < root.val:
            root.left = self.insertIntoBST(root.left, val)
        
        return root
```

## 450. Delete Node in a BST[[Link](https://leetcode.com/problems/delete-node-in-a-bst/description/)]
- video explaination[[Link](https://neetcode.io/problems/delete-node-in-a-bst?list=blind75)]

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def min_val(self, node):
        curr = node
        while curr and curr.left:
            curr = curr.left
        return curr

    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return None
        
        if key > root.val:
            root.right = self.deleteNode(root.right, key)
        elif key < root.val:
            root.left = self.deleteNode(root.left, key)
        else:
            if not root.right:
                return root.left
            elif not root.left:
                return root.right
            else:
                # get the min_node
                min_node = self.min_val(root.right)
                # set the curr node value to min_node's
                root.val = min_node.val
                # at this time, we have two copies of min_node, remove the origin one by recursivly call deleteNode
                root.right = self.deleteNode(root.right, min_node.val)
        return root
```