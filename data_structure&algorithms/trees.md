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

## Basic BST Operation

### Insert

__How it works:__
- Initilize the current node with root node
- Compare the key with the current node.
- Move left if the key is less than or equal to the current node value.
- Move right if the key is greater than current node value.

__Non-recursive method:__
```java
class BST {
    TreeNode root;

    void insert(int val) {
        TreeNode newNode = new TreeNode(val);
        if (root == null) { 
            root = new newNode;
            return;
        }

        TreeNode current = root;
        while (true) {
            if (newNode.val == current.val) 
                return false;
            
            if (newNode.val < current.val) {
                if (current.left == null) {
                    current.left = newNode;
                    return;
                }
                current = current.left;
            }
            else {
                if (current.right == null) {
                    current.right = newNode;
                    return;
                }
                current = current.right;
            }
        }
    }
}
```
<br/>

__Recursive method__
```java
class BST {
    TreeNode root;

    void insert(int val) {
        root = insertHelper(root, val);
    }

    private TreeNode insertHelper(TreeNode node, int val) { 
        TreeNode newNode = new TreeNode(val);
        if (node == null) {
            return newNode;
        }

        if (val < node.val) {
            node.left = insertHelper(node.left, val);
        }
        else {
            node.right = insertHelper(node.right, val);
        }
        return node;
    }
}
```
<br/>

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
<br/>

### 100. Same Tree [[link](https://leetcode.com/problems/same-tree/?envType=study-plan-v2&envId=top-interview-150)]

__How it works:__
- Base Case: 
    - If both nodes are null, they represent the same “empty” branch.
    - If one is null but not the other, or if their values don’t match, then the trees differ.
- Recursively check left subtrees and right subtrees

__Answer:__
```java
class Solution {
    public boolean isSameTree(TreeNode p, TreeNode q) {
        if (p == null && q == null)
            return true;

        if (p == null || q == null || (p.val != q.val))
            return false;
        
        return isSameTree(p.right, q.right) && isSameTree(p.left, q.left);
    }
}
```
<br/>

### 226. Invert Binary Tree [[link](https://leetcode.com/problems/invert-binary-tree/?envType=study-plan-v2&envId=top-interview-150)]

__How it works:__


__Answer:__
```java
class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null)
            return null;
        TreeNode left = invertTree(root.left);
        TreeNode right = invertTree(root.right);
        root.left = right;
        root.right = left;
        return root;
    }
}
```
<br/>