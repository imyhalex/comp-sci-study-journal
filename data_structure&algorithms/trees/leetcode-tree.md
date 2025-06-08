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

## 94. Binary Tree Inorder Traversal[[Link](https://leetcode.com/problems/binary-tree-inorder-traversal/description/)]
- video explaination[[Link](https://neetcode.io/problems/binary-tree-inorder-traversal?list=blind75)]
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []

        def dfs(node):
            if not node:
                return None
            
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)
        
        dfs(root)
        return res
```

## 230. Kth Smallest Element in a BST[[Link](https://leetcode.com/problems/kth-smallest-element-in-a-bst/description/)]
- video explaination[[Link](https://neetcode.io/problems/kth-smallest-integer-in-bst?list=blind75)]

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        res = []

        def dfs(node):
            if not node:
                return None
            
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)
        
        dfs(root)
        return res[:k][-1]
```

## 105. Construct Binary Tree from Preorder and Inorder Traversal[[Link](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/?envType=study-plan-v2&envId=top-interview-150)]
- video explaination[[Link](https://neetcode.io/problems/binary-tree-from-preorder-and-inorder-traversal?list=blind75)]

```python
# time: O(n ^ 2); space: O(n)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder or not inorder:
            return None

        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])
        root.left = self.buildTree(preorder[1: mid + 1], inorder[: mid])
        root.right = self.buildTree(preorder[mid + 1: ], inorder[mid + 1: ])
        return root
```

## 106. Construct Binary Tree from Inorder and Postorder Traversal[[Link](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/?envType=study-plan-v2&envId=top-interview-150)]

```python
# time: O(n ^ 2); space: O(n)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        if not inorder or not postorder:
            return None
        
        root = TreeNode(postorder[-1])
        mid = inorder.index(postorder[-1])
        root.left = self.buildTree(inorder[: mid], postorder[: mid])
        root.right = self.buildTree(inorder[mid+1:], postorder[mid:-1])
        return root
```

## 226. Invert Binary Tree[[Link](https://leetcode.com/problems/invert-binary-tree/description/?envType=study-plan-v2&envId=top-interview-150)]
- video explaination[[Link](https://neetcode.io/problems/invert-a-binary-tree?list=blind75)]

```python
# time: O(n); Space: O(h)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        
        if root:
            tmp = root.left
            root.left= self.invertTree(root.right)
            root.right = self.invertTree(tmp)
        
        return root
```

## 104. Maximum Depth of Binary Tree[[Link](https://leetcode.com/problems/maximum-depth-of-binary-tree/description/?envType=study-plan-v2&envId=top-interview-150)]
- video explaination[[Link](https://neetcode.io/problems/depth-of-binary-tree?list=blind75)]

```python
# time: O(n); Space: O(h)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

## 543. Diameter of Binary Tree[[Link](https://leetcode.com/problems/diameter-of-binary-tree/description/)]

- video explaination[[Link](https://neetcode.io/problems/binary-tree-diameter?list=blind75)]

```python
# time: O(n); Space: O(h)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.max_diameter = 0

        def dfs(node):
            if not node:
                return 0
            
            left = dfs(node.left)
            right = dfs(node.right)

            # update max diameter (edge = left + right)
            self.max_diameter = max(self.max_diameter, left + right)

            return 1 + max(left, right) # height of this node
        
        dfs(root)
        return self.max_diameter
```

## 110. Balanced Binary Tree[[Link](https://leetcode.com/problems/balanced-binary-tree/description/)]
- video explaination[[Link](https://neetcode.io/problems/balanced-binary-tree?list=blind75)]

```python
# time: O(n); Space: O(h)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        
        def dfs(node):
            if not node:
                return [True, 0]
            
            left = dfs(node.left)
            right = dfs(node.right)
            is_balanced = left[0] and right[0] and abs(left[1] - right[1]) <= 1
            return [is_balanced, 1 + max(left[1], right[1])]
        
        return dfs(root)[0]
```

## 100. Same Tree[[Link](https://leetcode.com/problems/same-tree/description/)]
- video explaination[[Link](https://neetcode.io/problems/same-binary-tree?list=blind75)]

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        if p and q and p.val == q.val: 
            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        return False
```

## 572. Subtree of Another Tree[[Link](https://leetcode.com/problems/subtree-of-another-tree/description/)]
- video explaination[[Link](https://neetcode.io/problems/subtree-of-a-binary-tree?list=blind75)]

```python
# time: O(n *m); space: O(n + m)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        
        def is_same_tree(a, b):
            if not a and not b:
                return True
            if a and b and a.val == b.val:
                return is_same_tree(a.left, b.left) and is_same_tree(a.right, b.right)
            return False
        
        if not root:
            return False
        if not subRoot:
            return True
        
        if is_same_tree(root, subRoot):
            return True
        return (self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot))
```

## 235. Lowest Common Ancestor of a Binary Search Tree[[Link](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/description/)]
- video explaination[[Link](https://neetcode.io/problems/lowest-common-ancestor-in-binary-search-tree?list=blind75)]

```python
# time: O(h); space: O(1)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        curr = root

        while curr:
            if p.val < curr.val and q.val < curr.val:
                curr = curr.left
            elif p.val > curr.val and q.val > curr.val:
                curr = curr.right
            else:
                return curr

# or
# time & space: O(h)
class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        if p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestor(root.left, p, q)
        elif p.val > root.val and q.val > root.val:
            return self.lowestCommonAncestor(root.right, p, q)
        else:
            return root
```

## 236. Lowest Common Ancestor of a Binary Tree[[Link](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/description/)]
- video explaination[[Link](https://www.youtube.com/watch?v=WO1tfq2sbsI)]

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root or root == p or root == q:
            return root
        
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        if left and right:
            return root # p and q found in different subtree
        
        return left if left else right # one node found in subtree
```

## 102. Binary Tree Level Order Traversal[[Link](https://leetcode.com/problems/binary-tree-level-order-traversal/description/?envType=study-plan-v2&envId=top-interview-150)]
- video explaination[[Link](https://neetcode.io/problems/level-order-traversal-of-binary-tree?list=blind75)]

```python
# time & space: O(n)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        res = []
        q = deque()
        q.append(root)

        while q:
            level = []
            for _ in range(len(q)):
                node = q.popleft()
                if node:
                    level.append(node.val)
                    q.append(node.left)
                    q.append(node.right)
            if level:
                res.append(level)
        
        return res
```

## 199. Binary Tree Right Side View[[Link](https://leetcode.com/problems/binary-tree-right-side-view/description/?envType=study-plan-v2&envId=top-interview-150)]
- video explaination[[Link](https://neetcode.io/problems/binary-tree-right-side-view?list=blind75)]

```python
# time & space: O(n)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        q = deque()
        q.append(root)

        while q:
            right_side = None
            for _ in range(len(q)):
                node = q.popleft() 
                if node:
                    right_side = node
                    q.append(node.left)
                    q.append(node.right)
            if right_side:
                res.append(right_side.val)
        
        return res
```

## 1448. Count Good Nodes in Binary Tree[[Link](https://leetcode.com/problems/count-good-nodes-in-binary-tree/description/)]
- video explaination[[Link](https://neetcode.io/problems/count-good-nodes-in-binary-tree?list=blind75)]

```python
# time & space: O(n)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:

        def dfs(node, max_val):
            if not node:
                return 0
            
            count = 1 if node.val >= max_val else 0 # means for every node, you deserve to get value 1 if your node val is larger than the current max val
            max_val = max(max_val, node.val)
            count += dfs(node.left, max_val)
            count += dfs(node.right, max_val)
            return count
        
        return dfs(root, root.val)

```

## 98. Validate Binary Search Tree[[Link](https://leetcode.com/problems/validate-binary-search-tree/description/)]

- video explaination[[Link](https://neetcode.io/problems/valid-binary-search-tree?list=blind75)]

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        
        def dfs(node, res):
            if node:
                dfs(node.left, res)
                res.append(node.val)
                dfs(node.right, res)
        
        res = []
        dfs(root, res)
        for i in range(1, len(res)):
            if res[i] <= res[i - 1]:
                return False
        
        return True
```

## 124. Binary Tree Maximum Path Sum[[Link](https://leetcode.com/problems/binary-tree-maximum-path-sum/description/?envType=study-plan-v2&envId=top-interview-150)] 
- video explaination[[Link](https://neetcode.io/problems/binary-tree-maximum-path-sum?list=blind75)]

```python
# time & space: O(n)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_sum = root.val

        def dfs(node):
            if not node:
                return 0

            left = dfs(node.left) 
            right = dfs(node.right)
            left = max(left, 0)
            right = max(right, 0)
            # Candidate max path sum using both children + current node
            self.max_sum = max(self.max_sum, node.val + left + right)
            # Only return one-side path to parent
            return node.val + max(left, right)
        
        dfs(root)
        return self.max_sum
```

## 297. Serialize and Deserialize Binary Tree[[Link](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/description/)]

- video explaination[[Link](https://neetcode.io/problems/serialize-and-deserialize-binary-tree?list=blind75)]

```python
# time & space: O(n)
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        res = []

        def dfs(node):
            if not node:
                res.append("#")
                return
            
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        
        dfs(root)
        return ",".join(res)

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        values = iter(data.split(","))

        def dfs():
            value = next(values)
            if value == "#":
                return None
            node = TreeNode(int(value))
            node.left = dfs()
            node.right = dfs()
            return node
        
        return dfs()
        

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))
```