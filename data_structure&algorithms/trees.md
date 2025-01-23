# Binary Search Tree
- Big O: log n

## A typical structure in:

```java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode() {}

    TreeNode(int val) {
        this.val = val;
    }

    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
```

## Leetcode Questions

### 104. Maximum Depth of Binary Tree [[link](https://leetcode.com/problems/maximum-depth-of-binary-tree/?envType=study-plan-v2&envId=top-interview-150)]

__How it works:__
- Base Case: If root is null, that path contributes a depth of 0
- Recursively get the depth of left subtree
- Revursively get the depth of right subtree
- Add 1 for the current node (for the depth incremental)

__Answer:__
```java
class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null)
            return 0;
        
        int leftDepth = maxDepth(root.left);
        int rightDepth = maxDepth(root.right);

        return 1 + (leftDepth > rightDepth? leftDepth : rightDepth);
    }
}
```
---
### 104. Maximum Depth of Binary Tree [[link](https://leetcode.com/problems/maximum-depth-of-binary-tree/?envType=study-plan-v2&envId=top-interview-150)]

__How it works:__
- Base Case: If root is null, that path contributes a depth of 0
- Recursively get the depth of left subtree
- Revursively get the depth of right subtree
- Add 1 for the current node (for the depth incremental)

__Answer:__
```java
class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null)
            return 0;
        
        int leftDepth = maxDepth(root.left);
        int rightDepth = maxDepth(root.right);

        return 1 + (leftDepth > rightDepth? leftDepth : rightDepth);
    }
}
```