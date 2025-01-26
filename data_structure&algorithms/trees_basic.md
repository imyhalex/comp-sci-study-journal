# Binary Search Tree
- Big O for traversal: log n

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

__How it works[[Video Explaination](https://www.youtube.com/watch?v=TREbF6S_5qo)]__

__Answer in $O(n)$ time complexity:__
Below is the **optimized** approach using a `HashMap` to achieve \(O(n)\) time complexity. The idea is:

1. **Preprocessing**: Build a `HashMap` that maps each value in the `inorder` array to its index. This takes \(O(n)\) time.
2. **Preorder**: The first element in the `preorder` slice is always the root.
3. **Lookup**: Find the root’s index in `inorder` by directly querying the `HashMap` in \(O(1)\) time.
4. **Recurse**:
   - Compute the size of the left subtree.
   - Recursively construct left subtree and right subtree by slicing the `preorder` array appropriately (and using the corresponding `inorder` boundaries).

This avoids the \(O(n)\) scan of the `inorder` array at each recursive step, bringing the total complexity down to **\(O(n)\)**.

__Time Complexity__

1. **Building the HashMap**: \(O(n)\).  
2. **Recursive Construction**:
   - Each node is processed exactly once, and looking up the root’s index in the `inorder` array is \(O(1)\) due to the HashMap.  
   - Hence, this step also takes \(O(n)\).  

Overall **Time Complexity: \(O(n)\)**.

__Space Complexity__

- \(O(n)\) for the HashMap.  
- \(O(h)\) for the recursion call stack, where \(h\) is the tree height (worst-case \(O(n)\) if the tree is skewed).  

Thus total space complexity is **\(O(n)\)** in the worst case.


```java
import java.util.HashMap;

class Solution {
    // acts as a lookup table
    HashMap<Integer, Integer> inOrderIndexMap;

    private TreeNode buildTreeHelper(int[] preorder, int preStart, int preEnd, int[] inorder, int inStart, int inEnd) {
        // if there are no element in the subtree
        if (preStart > preEnd || inStart > inEnd)
            return null;
        
        // use preorder to locate the root
        int rootVal = preorder[preStart];
        TreeNode root = new TreeNode(rootVal);

        // look up the root's index in the inorder array in o(1) time
        int rootIndexInOrder = inOrderIndexMap.get(rootVal);

        // number of nodes in th left subtree
        int leftTreeSize = rootIndexInOrder - inStart;

        // build left subtree
        root.left = buildTreeHelper(preorder, preStart + 1, preStart + leftTreeSize, inorder, inStart, rootIndexInOrder - 1);

        // build the right subtree
        root.right = buildTreeHelper(preorder, preStart + leftTreeSize + 1, preEnd, inorder, rootIndexInOrder + 1, inEnd);

        return root;
    }

    public TreeNode buildTree(int[] preorder, int[] inorder) {
        if (preorder == null || inorder == null || preorder.length != inorder.length)
            return null;
        
        inOrderIndexMap = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) 
            inOrderIndexMap.put(inorder[i], i);

        return buildTreeHelper(preorder, 0, preorder.length - 1, inorder, 0, inorder.length - 1);
    }
}
```
<br/>


### 106. Construct Binary Tree from Inorder and Postorder Traversal[[link](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/?envType=study-plan-v2&envId=top-interview-150)]

__How it works:__

__Answer:__
```java
import java.util.HashMap;

class Solution {
    private HashMap<Integer, Integer> inOrderIndexMap;

    private TreeNode buildTreeHelper(int[] inorder, int inStart, int inEnd, int[] postorder, int postStart, int postEnd) {
        if (inStart > inEnd || postStart > postEnd)
            return null;

        // root always starts with the last element of postorder
        int rootVal = postorder[postEnd];
        TreeNode root = new TreeNode(rootVal);

        int rootIndexInOrder = inOrderIndexMap.get(rootVal);
        int leftTreeSize = rootIndexInOrder - inStart;

        root.left = buildTreeHelper(inorder, inStart, rootIndexInOrder - 1, postorder, postStart, postStart + leftTreeSize - 1);
        root.right = buildTreeHelper(inorder, rootIndexInOrder + 1, inEnd, postorder, postStart + leftTreeSize, postEnd - 1);

        return root;
    }

    public TreeNode buildTree(int[] inorder, int[] postorder) {
       if (inorder == null || postorder == null || inorder.length != postorder.length)
            return null;

        inOrderIndexMap = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) 
            inOrderIndexMap.put(inorder[i], i);
        
        return buildTreeHelper(inorder, 0, inorder.length - 1, postorder, 0, postorder.length - 1);
    }
}
```
<br/>

### 117. Populating Next Right Pointers in Each Node II[[Link](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/description/?envType=study-plan-v2&envId=top-interview-150)]

__Answer in BFS (Level-Order) Solution:__
- Use a queue to store nodes level by level.
- Pop nodes from the queue to process each level.
- Link each node’s next pointer to the subsequent node in the queue (except for the last node in each level, whose next is set to null).
- Push the child nodes (left and right) to the queue for the next level.

```java
import java.util.LinkedList;
import java.util.Queue;

class Node {
    int val;
    Node left;
    Node right;
    Node next;

    Node() {}

    Node (int val) { 
        this.val = val;
    }

    Node(int val, Node left, Node right, Node next) { 
        this.val = val;
        this.left = left;
        this.right = right;
        this.next = next;
    }
}

class Solution { 
    public Node connect(Node root) {
        if (root == null)
            return null;

        Queue<Node> queue = new LinkedList<>();
        queue.add(root);

        while (!queue.isEmpty()) {
            int levelSize = queue.size();

            // iterate over all nodes in the current level
            for (int i = 0; i < levelSize; i++) {
                Node current = queue.poll();

                // link the current node's next to the next node in the queue
                // except for the last node in this level
                if (i < levelSize - 1)
                    current.next = queue.peek();
                else 
                    current.next = null;
                
                // add children to the queue
                if (current.left != null)
                    queue.add(current.left);
                if (current.right != null)
                    queue.add(current.right);
            }
        }

        return root;
    }
}
```
<br/>

### 114. Flatten Binary Tree to Linked List[[Link](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/?envType=study-plan-v2&envId=top-interview-150)]

__Video Explaination[[Link](https://www.youtube.com/watch?v=rKnD7rLT0lI)]__
```java
class Solution {
    // pre-order style: flattern the root tree and return the list tail
    private TreeNode flatternTree(TreeNode node) {
        if (node == null)
            return null;
        
        if (node.left == null && node.right == null)
            return node;
        
        TreeNode leftTail = flatternTree(node.left);
        TreeNode rightTail = flatternTree(node.right);

        if (leftTail != null) {
            leftTail.right = node.right;
            node.right = node.left;
            node.left = null;
        }

        return rightTail == null ? leftTail : rightTail;
    }

    public void flatten(TreeNode root) {
        flatternTree(root);
    }
}
```
<br/>

### 112. Path Sum[[Link](https://leetcode.com/problems/path-sum/description/?envType=study-plan-v2&envId=top-interview-150)]

__Approach 1 - Recursion:__
```java
class Solution {
    public boolean hasPathSum(TreeNode root, int targetSum) {
        if (root == null) 
            return false;

        targetSum -= root.val;
        if (root.left == null && root.right == null)
            return targetSum == 0;
        return hasPathSum(root.left, targetSum) || hasPathSum(root.right, targetSum);
    }
}
```
<br/>

__Approach 2 - Iterative (using stack):__
```java
import java.util.Stack;

class Solution {
    Stack<TreeNode> node_stack = new Stack<>();
    Stack<Integer> sum_stack = new Stack<>();

    public boolean hasPathSum(TreeNode root, int targetSum) {
        if (root == null)
            return false;
        node_stack.push(root);
        sum_stack.push(targetSum);
        
        TreeNode node;
        int current_sum;
        while (!node_stack.isEmpty()) { 
            node = node_stack.pop();
            current_sum = sum_stack.pop();

            if (node.right == null && node.left == null && current_sum == 0)
                return true;
            
            if (node.right != null) { 
                node_stack.add(node.right);
                sum_stack.add(current_sum - node.right.val);
            }

            if (node.left != null) { 
                node_stack.add(node.left);
                sum_stack.add(current_sum - node.left.val);
            }
        }

        return false;
    }
}
```
<br/>

### 129. Sum Root to Leaf Numbers[[Link](https://leetcode.com/problems/sum-root-to-leaf-numbers/description/?envType=study-plan-v2&envId=top-interview-150)]

__How it works:__
- DFS in preorder

__Answer:__
```java
class Solution {
    int rootToLeaf = 0;

    private void sumNumbersHelper(TreeNode node, int currentSum) { 
        if (node != null) { 
            currentSum = currentSum * 10 + node.val;
            if (node.left == null && node.right == null) 
                rootToLeaf += currentSum;
            sumNumbersHelper(node.left, currentSum);
            sumNumbersHelper(node.right, currentSum);
        }
    }

    public int sumNumbers(TreeNode root) {
        sumNumbersHelper(root, 0);
        return rootToLeaf;
    }
}
```
<br/>

### 124. Binary Tree Maximum Path Sum[[Link](https://leetcode.com/problems/binary-tree-maximum-path-sum/description/?envType=study-plan-v2&envId=top-interview-150)]

__How it works[[Video Link](https://www.youtube.com/watch?v=Hr5cWUld4vU)]:__ 
- DFS in postorder
- Main function body:
    - Initialize a global variable max_sum to -Infinity.
    - Call the function gain_from_subtree on the tree's root.
    - Return the value of max_sum.
- Body of the recursive function gain_from_subtree. It accepts root of the subtree as the input.
    - If the root is null, return 0. This is the base case. If a node doesn't have a left or right child, then the path sum contributed by the respective subtree is 0.
    - Call the function recursively on the left and right child of the root. Store the results in gain_from_left and gain_from_right, respectively.
    - If either is negative, set it to 0. This is because we don't want to include a path sum contributed by a subtree if it is negative.
    - Update the maximum path sum (max_sum) seen so far. To do so, compare max_sum with the sum of the following, and update it if it is smaller.
    - Return the path sum gain contributed by the subtree. This is the maximum of the following two values.

__Answer:__
```java
class Solution {
    int maxSum;

    private int maxPathSumHelper(TreeNode node) { 
        if (node == null)
            return 0;
        
        int gainFromLeft = Math.max(maxPathSumHelper(node.left), 0);
        int gainFromRight = Math.max(maxPathSumHelper(node.right), 0);

        maxSum = Math.max(maxSum, gainFromLeft + gainFromRight + node.val);
        
        return Math.max(gainFromLeft + node.val, gainFromRight + node.val);
    }

    public int maxPathSum(TreeNode root) {
        maxSum = Integer.MIN_VALUE;
        maxPathSumHelper(root);
        return maxSum;
    }
}
```
<br/>


### 173. Binary Search Tree Iterator[[Link](https://leetcode.com/problems/binary-search-tree-iterator/description/?envType=study-plan-v2&envId=top-interview-150)]

```java
class BSTIterator {
    ArrayList<Integer> list;
    int index;

    private void inorder(TreeNode node) { 
        if (node != null) { 
            inorder(node.left);
            list.add(node.val);
            inorder(node.right);
        }
    }
    
    public BSTIterator(TreeNode root) {
        this.list = new ArrayList<>();
        this.index = -1;
        this.inorder(root);
    }
    
    public int next() {
        return list.get(++index);
    }
    
    public boolean hasNext() {
        return index + 1 < list.size();
    }
}
```
<br/>


### 222. Count Complete Tree Nodes[[Link](https://leetcode.com/problems/count-complete-tree-nodes/description/?envType=study-plan-v2&envId=top-interview-150)]

__Explaination of Complete Tree:[[Link](https://www.geeksforgeeks.org/complete-binary-tree/)]__
- find the height of root node by only traversing the leftmost branch of the tree because a complete tree is always filled value from left to right as I mentioned. We call this value is \(h\)

- After that, we continue to find the heigth of right branch.

- If right branch is h - 1, the left branch is the balance tree with height h - 1, then total nodes of left branch is 2^(h-1+1) - 1 = 2^h - 1. And the total nodes of tree from root node is (2^h + total nodes on right branch)
If right branch is h - 2, then the last node is on left branch. So, total nodes of right branch is 2^(h-2+1) - 1 = 2^(h-1) - 1. And the total nodes of tree from root node is (2^(h-1) + total nodes on left branch)
__Answer:__
```java
class Solution {

    private int height(TreeNode node) { 
        return node == null ? -1 : 1 + height(node.left);
    }

    public int countNodes(TreeNode root) {
        int h = height(root);
        return h < 0 ? 0 : height(root.right) == h - 1 ? 
                        (1 << h) + countNodes(root.right) : (1 << h - 1) + countNodes(root.left);
    }
}
```
<br/>

### 236. Lowest Common Ancestor of a Binary Tree[[Link](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/description/?envType=study-plan-v2&envId=top-interview-150)]

__Video Explaination[[Link](https://www.youtube.com/watch?v=gs2LMfuOR9k)]__
```java
class Solution {

    private TreeNode dfs(TreeNode node, TreeNode p, TreeNode q) { 
        // 1. Base case
        if (node == null)
            return null;
        
        // 2. If the current node is p or q, return it
        if (node == p || node == q)
            return node;
        
        // 3. Search in left and right subtrees
        TreeNode leftNode = dfs(node.left, p, q);
        TreeNode rightNode = dfs(node.right, p, q);

         // 4. If both sides returned a node, current node is the LCA
        if (leftNode != null && rightNode != null)
            return node;

        // 5. Otherwise, return the non-null side (could be null if neither side has p or q)
        return leftNode != null ? leftNode : rightNode;
    }

    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        return dfs(root, p, q);
    }
}
```
<br/>