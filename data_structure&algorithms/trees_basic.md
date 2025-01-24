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

    // the passed in node should remain the same as it origin points to
    private TreeNode insertHelper(TreeNode node, int val) { 
        if (node == null) {
            return new TreeNode(val);
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

### Search

__How it works:__
- Compare the value to be searched with the value of the root
- Repeat the above step till no more traversal is possible
- If at any iteration, key is found, return True. Else False.

__Non-recursive method:__
```java
class BST {
    TreeNode root;

    boolean search(int value) {
        // start from the null
        TreeNode current = root;

        while (current != null) {
            if (current.val == value)
                return true;
            else if (value < current.val)
                current = current.left;
            else
                current = current.right;
        }

        return false;
    }
}
```
<br/>

__Recursive Methods__
```java
class BST {
    TreeNode root;

    boolean rsearch(int value) {
        return rsearchHelper(root, value);
    }

    private boolean rsearchHelper(TreeNode node, int value) {
        if (node == null)
            return false;
        if (node.val == value)
            return true;
        if (value < node.val)
            return rsearchHelper(node.left, value);
        else
            return rsearchHelper(node.right, value);
    } 
}
```
<br/>

### Delete

__How it works:__
Below is a standard **recursive** implementation of the BST deletion algorithm in Java. It handles all the usual cases:

1. **Node not found**: If the tree or subtree is `null`, just return `null`.
2. **Node has no children (leaf)**: Simply remove it by returning `null`.
3. **Node has one child**: Return the non-null child (left or right) to replace the node.
4. **Node has two children**:
   - Find the minimum value in the right subtree (or alternatively, the maximum value in the left subtree).
   - Replace the current node’s value with that minimum value.
   - Recursively delete that minimum value from the right subtree.

```java
class BST {
    TreeNode root;
    
    void delete(int value) {
        root = deleteNode(root, value);
    }

    // the passed in node should remain the same as it origin points to
    private TreeNode deleteNode(TreeNode node, int value) {
        if (node == null)
            return null;
        
        if (value < node.val)
            node.left = deleteNode(node.left, value);
        else if (value > node.val)
            node.right = deleteNode(node.right, value);
        else {
            // case 1. no left child
            if (node.left == null)
                return node.right;
            // case 2: no right child
            else if (node.right == null)
                return node.left;
            // case 3: two children
            int minVal = findMin(node.right);
            // replace the current node's alue with the minimum from right subtree
            node.val = minVal;
            // delete that minimum value from the right subtree
            node.right = deleteNode(node.right, minVal);
        }

        return node;
    }

    private int findMin(TreeNode node) {
        int min = node.val;
        while (node.left != null) {
            node = node.left;
            min = node.val;   
        }
        return min;
    }
}
```

### How It Works

1. **Search for the node**: We compare `val` with the current node’s value and traverse left or right accordingly.  
2. **Delete Cases**:
   - **No Child (Leaf)**: If the node has no children, return `null` to remove it.
   - **One Child**: If the node has one child, return that child in place of the current node.
   - **Two Children**:
     1. Find the minimum value in the right subtree.  
     2. Replace the current node’s `val` with that minimum value.  
     3. Recursively delete that minimum value from the right subtree (to avoid duplicates).  
3. **Return the node**: Because we may have changed the node (or replaced it with a child), we return the node back up the call stack so parent references are updated properly.

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

### 101. Symmetric Tree [[link](https://leetcode.com/problems/symmetric-tree/description/?envType=study-plan-v2&envId=top-interview-150)]

__How it works__
- Treat it as two trees shared one root
- Compare each mirrored element respectivley

__Answer:__
```java
class Solution {
    public boolean isSymmetric(TreeNode root) {
        return isSymmetricHelper(root, root);
    }

    private boolean isSymmetricHelper(TreeNode node, TreeNode node1) {
        if (node == null && node1 == null) return true;
        if (node == null || node1 == null) return false;
        return (node.val == node1.val) && isSymmetricHelper(node.right, node1.left) && isSymmetricHelper(node.left, node1.right);
    }
}
```
<br/>

### 105. Construct Binary Tree from Preorder and Inorder Traversal [[link](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/?envType=study-plan-v2&envId=top-interview-150)]

__How it works__

__Answer:__
```java
class Solution {
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        
    }
}
```
<br/>